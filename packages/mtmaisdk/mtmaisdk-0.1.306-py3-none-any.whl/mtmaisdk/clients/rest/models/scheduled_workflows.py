# coding: utf-8

"""
    Hatchet API

    The Hatchet API

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from mtmaisdk.clients.rest.models.api_resource_meta import APIResourceMeta
from mtmaisdk.clients.rest.models.workflow_run_status import WorkflowRunStatus
from typing import Optional, Set
from typing_extensions import Self

class ScheduledWorkflows(BaseModel):
    """
    ScheduledWorkflows
    """ # noqa: E501
    metadata: APIResourceMeta
    tenant_id: StrictStr = Field(alias="tenantId")
    workflow_version_id: StrictStr = Field(alias="workflowVersionId")
    workflow_id: StrictStr = Field(alias="workflowId")
    workflow_name: StrictStr = Field(alias="workflowName")
    trigger_at: datetime = Field(alias="triggerAt")
    input: Optional[Dict[str, Any]] = None
    additional_metadata: Optional[Dict[str, Any]] = Field(default=None, alias="additionalMetadata")
    workflow_run_created_at: Optional[datetime] = Field(default=None, alias="workflowRunCreatedAt")
    workflow_run_name: Optional[StrictStr] = Field(default=None, alias="workflowRunName")
    workflow_run_status: Optional[WorkflowRunStatus] = Field(default=None, alias="workflowRunStatus")
    workflow_run_id: Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]] = Field(default=None, alias="workflowRunId")
    __properties: ClassVar[List[str]] = ["metadata", "tenantId", "workflowVersionId", "workflowId", "workflowName", "triggerAt", "input", "additionalMetadata", "workflowRunCreatedAt", "workflowRunName", "workflowRunStatus", "workflowRunId"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of ScheduledWorkflows from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of metadata
        if self.metadata:
            _dict['metadata'] = self.metadata.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ScheduledWorkflows from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "metadata": APIResourceMeta.from_dict(obj["metadata"]) if obj.get("metadata") is not None else None,
            "tenantId": obj.get("tenantId"),
            "workflowVersionId": obj.get("workflowVersionId"),
            "workflowId": obj.get("workflowId"),
            "workflowName": obj.get("workflowName"),
            "triggerAt": obj.get("triggerAt"),
            "input": obj.get("input"),
            "additionalMetadata": obj.get("additionalMetadata"),
            "workflowRunCreatedAt": obj.get("workflowRunCreatedAt"),
            "workflowRunName": obj.get("workflowRunName"),
            "workflowRunStatus": obj.get("workflowRunStatus"),
            "workflowRunId": obj.get("workflowRunId")
        })
        return _obj


