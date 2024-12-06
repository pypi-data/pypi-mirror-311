#  Copyright (c) ZenML GmbH 2023. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Models representing run metadata."""

from typing import Dict, Optional
from uuid import UUID

from pydantic import Field

from zenml.enums import MetadataResourceTypes
from zenml.metadata.metadata_types import MetadataType, MetadataTypeEnum
from zenml.models.v2.base.scoped import (
    WorkspaceScopedRequest,
)

# ------------------ Request Model ------------------


class RunMetadataRequest(WorkspaceScopedRequest):
    """Request model for run metadata."""

    resource_id: UUID = Field(
        title="The ID of the resource that this metadata belongs to.",
    )
    resource_type: MetadataResourceTypes = Field(
        title="The type of the resource that this metadata belongs to.",
    )
    stack_component_id: Optional[UUID] = Field(
        title="The ID of the stack component that this metadata belongs to."
    )
    values: Dict[str, "MetadataType"] = Field(
        title="The metadata to be created.",
    )
    types: Dict[str, "MetadataTypeEnum"] = Field(
        title="The types of the metadata to be created.",
    )
