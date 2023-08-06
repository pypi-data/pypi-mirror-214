import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from time import sleep

import argo_workflows
from argo_workflows.model.io_argoproj_workflow_v1alpha1_arguments import (
    IoArgoprojWorkflowV1alpha1Arguments,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_parameter import (
    IoArgoprojWorkflowV1alpha1Parameter,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow import (
    IoArgoprojWorkflowV1alpha1Workflow,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_create_request import (
    IoArgoprojWorkflowV1alpha1WorkflowCreateRequest,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_spec import (
    IoArgoprojWorkflowV1alpha1WorkflowSpec,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_stop_request import (
    IoArgoprojWorkflowV1alpha1WorkflowStopRequest,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_template_ref import (
    IoArgoprojWorkflowV1alpha1WorkflowTemplateRef,
)
from argo_workflows.model.object_meta import ObjectMeta
from force_processor_bindings.model import ForceParameters, ForceResMergeOptions  # noqa
from openeo_executor_bindings.model import OpenEOExecutorParameters
from pystac import Collection, Item
from sen2like_processor_bindings.model import BoundingBox as Sen2LikeBoundingBox  # noqa
from sen2like_processor_bindings.model import (  # noqa
    Sen2LikeParameters,
    sen2like_options,
)

from eodc import settings

logger = logging.getLogger(__name__)


@dataclass
class FaasProcessorDetails:
    name: str
    workflow_template_name: str


class FaasProcessor(Enum):
    Force = FaasProcessorDetails("force", "faas-force")
    Sen2Like = FaasProcessorDetails("sen2like", "faas-sen2like")
    OpenEO = FaasProcessorDetails("openeo", "faas-openeo-executor")


class FaasProcessorBase(ABC):
    @classmethod
    def get_instance(cls, processor_details):
        return cls(processor_details=processor_details)

    def __init__(self, processor_details: FaasProcessorDetails) -> None:
        self.configuration = argo_workflows.Configuration(
            host=settings.FAAS_URL, disabled_client_side_validations=True
        )
        self.configuration.verify_ssl = False

        self.api_client = argo_workflows.ApiClient(self.configuration)
        self.api_instance_workflows = (
            argo_workflows.api.workflow_service_api.WorkflowServiceApi(self.api_client)
        )
        self.processor_details = processor_details
        # TODO: Check here that this workflow template even exists on the server

    def submit_workflow(self, **kwargs):
        parameters = [
            IoArgoprojWorkflowV1alpha1Parameter(name=k, value=v)
            for k, v in kwargs.items()
        ]

        manifest = IoArgoprojWorkflowV1alpha1Workflow(
            metadata=ObjectMeta(
                generate_name=f"{self.processor_details.name.lower()}-"
            ),
            spec=IoArgoprojWorkflowV1alpha1WorkflowSpec(
                workflow_template_ref=IoArgoprojWorkflowV1alpha1WorkflowTemplateRef(
                    name=self.processor_details.workflow_template_name
                ),
                arguments=IoArgoprojWorkflowV1alpha1Arguments(parameters=parameters),
            ),
        )

        created_workflow = self.api_instance_workflows.create_workflow(
            namespace=settings.NAMESPACE,
            body=IoArgoprojWorkflowV1alpha1WorkflowCreateRequest(workflow=manifest),
            _check_return_type=False,
        )

        workflow_name = created_workflow.metadata.get("name")

        logger.info(
            f"Submitted {self.processor_details.name.upper()} workflow: {workflow_name}"
        )
        return workflow_name

    def wait_for_completion(self, workflow_name: str) -> None:
        """Repeatedly query workflow status until it changes to a completed state"""

        def get_workflow_status(workflow_name: str) -> dict:
            status = self.api_instance_workflows.get_workflow(
                namespace=self.namespace,
                name=workflow_name,
                fields="status.phase,status.finishedAt,status.startedAt",
                _check_return_type=False,
            ).get("status", {})
            return status

        while (status := get_workflow_status(workflow_name)).get("finishedAt") is None:
            logger.info("Workflow still running, sleeping 30 seconds")
            sleep(30)
        logger.info(f"Workflow completed with status {status.get('phase')}.")

        if status.get("phase") in ("Failed", "Error"):
            raise ValueError(
                f"Workflow {workflow_name} ended with status {status.get('phase')}"
            )

    def stop_workflow(self, name):
        body = IoArgoprojWorkflowV1alpha1WorkflowStopRequest()
        self.api_instance_workflows.stop_workflow(settings.NAMESPACE, name, body=body)
        logger.info(f"Successfully stopped workflow {name}.")
        return

    def get_logs(self, workflow_name):
        # This Client method seems semi-broken: https://github.com/argoproj/argo-workflows/issues/7781
        return (
            self.api_instance_workflows.workflow_logs(
                settings.NAMESPACE,
                workflow_name,
                log_options_container="main",
                #  log_options_follow=True,
                _check_return_type=False,
                _preload_content=False,
            )
            .read()
            .decode("utf-8")
            .splitlines()
        )

    @abstractmethod
    def get_output_stac_items(self):
        pass


class Force(FaasProcessorBase):
    @classmethod
    def get_instance(cls):
        return cls(processor_details=FaasProcessor.Force.value)

    def submit_workflow(
        self, force_parameters: ForceParameters, user_id: str, job_id: str
    ):
        return super().submit_workflow(
            force_parameters=force_parameters.json(), user_id=user_id, job_id=job_id
        )

    def get_output_stac_items(self, force_parameters: ForceParameters) -> list[Item]:
        output_path = force_parameters.stac_output_dir

        collection_file = list(output_path.glob("*_collection.json"))[0]
        force_output_collection = Collection.from_file(str(collection_file))
        stac_items = [
            Item.from_file(link.get_absolute_href())
            for link in force_output_collection.get_item_links()
        ]

        return stac_items


class Sen2Like(FaasProcessorBase):
    @classmethod
    def get_instance(cls):
        return cls(processor_details=FaasProcessor.Sen2Like.value)

    def submit_workflow(
        self, sen2like_parameters: Sen2LikeParameters, user_id: str, job_id: str
    ):
        return super().submit_workflow(
            sen2like_parameters=sen2like_parameters.json(),
            user_id=user_id,
            job_id=job_id,
        )

    def get_output_stac_items(
        self, sen2like_parameters: Sen2LikeParameters, target_product: str = "L2F"
    ) -> list[Item]:
        from sen2like_processor_bindings.model import get_output_stac_item_paths

        stac_item_paths = get_output_stac_item_paths(
            sen2like_parameters, target_product=target_product
        )
        stac_items = [Item.from_file(path) for path in stac_item_paths]
        return stac_items


class OpenEO(FaasProcessorBase):
    @classmethod
    def get_instance(cls):
        return cls(processor_details=FaasProcessor.OpenEO.value)

    def submit_workflow(
        self,
        openeo_parameters: OpenEOExecutorParameters,
        openeo_user_id: str,
        openeo_job_id: str,
    ):
        return super().submit_workflow(
            openeo_executor_parameters=openeo_parameters.json(),
            openeo_user_id=openeo_user_id,
            openeo_job_id=openeo_job_id,
        )
