from typing import List

from pydantic import BaseModel

from .service import CoreApiService


class DeployRequest(BaseModel):
    app_name: str
    container_image: str
    num_cpu_cores: int
    num_gpu: int
    # TODO: Share SKU enums from main repo.
    gpu: str
    # cpu: str
    memory: int
    replicas: int


class DeployResponse(BaseModel):
    app_name: str


class DeleteResponse(BaseModel):
    # TODO: Needs better definition once the spec starts to settle.
    status: dict


class ListDeploymentsResponse(BaseModel):
    deployments: List[str]


class LogsResponse(BaseModel):
    logs: dict


class PredictResponse(BaseModel):
    result: dict


class DeploymentServiceV1(CoreApiService):
    base_path: str = "/api/v1/deployments"

    def deploy(self, deploy_request: DeployRequest) -> DeployResponse:
        r = self._post("/deploy", json=deploy_request.dict())
        # TODO: Add better status checks and failed login reporting.
        r.raise_for_status()
        j = r.json()
        return DeployResponse(app_name=j["app_name"])

    def list(self) -> ListDeploymentsResponse:
        r = self._get("/deployments")
        # TODO: Add better status checks and failed login reporting.
        r.raise_for_status()
        j = r.json()
        return ListDeploymentsResponse(deployments=j["deployments"])

    def delete(self, app_name: str):
        r = self._delete(f"/{app_name}")
        # TODO: Add better status checks and failed login reporting.
        r.raise_for_status()
        j = r.json()
        return DeleteResponse(status=j["status"])

    def logs(self, app_name: str):
        r = self._get(f"/{app_name}/logs")
        # TODO: Add better status checks and failed login reporting.
        r.raise_for_status()
        j = r.json()
        return LogsResponse(logs=j["logs"])

    def predict(self, app_name: str, data: dict):
        r = self._post(f"/{app_name}/predict", json=data)
        # TODO: Add better status checks and failed login reporting.
        r.raise_for_status()
        return PredictResponse(result=r.json())
