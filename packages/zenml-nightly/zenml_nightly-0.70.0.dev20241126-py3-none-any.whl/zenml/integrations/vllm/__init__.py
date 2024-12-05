#  Copyright (c) ZenML GmbH 2024. All Rights Reserved.
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
"""Initialization for the ZenML vLLM integration."""
from typing import List, Type
from zenml.integrations.integration import Integration
from zenml.stack import Flavor
from zenml.logger import get_logger
from zenml.integrations.constants import VLLM

VLLM_MODEL_DEPLOYER = "vllm"

logger = get_logger(__name__)


class VLLMIntegration(Integration):
    """Definition of vLLM integration for ZenML."""

    NAME = VLLM

    REQUIREMENTS = ["vllm>=0.6.0,<0.7.0", "openai>=1.0.0"]

    @classmethod
    def activate(cls) -> None:
        """Activates the integration."""
        from zenml.integrations.vllm import services

    @classmethod
    def flavors(cls) -> List[Type[Flavor]]:
        """Declare the stack component flavors for the vLLM integration.

        Returns:
            List of stack component flavors for this integration.
        """
        from zenml.integrations.vllm.flavors import VLLMModelDeployerFlavor

        return [VLLMModelDeployerFlavor]


VLLMIntegration.check_installation()
