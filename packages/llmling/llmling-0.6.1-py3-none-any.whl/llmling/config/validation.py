"""Configuration validation utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

import logfire

from llmling.core import exceptions
from llmling.core.log import get_logger


if TYPE_CHECKING:
    from llmling.config.models import Config


logger = get_logger(__name__)


class ConfigValidator:
    """Configuration validator."""

    def __init__(self, config: Config) -> None:
        """Initialize validator.

        Args:
            config: Configuration to validate
        """
        self.config = config

    def validate_all(self) -> list[str]:
        """Run all validations.

        Returns:
            List of validation warnings
        """
        warnings = []
        warnings.extend(self._validate_resources())
        warnings.extend(self._validate_processors())
        return warnings

    def _validate_resources(self) -> list[str]:
        """Validate resource configuration.

        Returns:
            List of validation warnings
        """
        warnings: list[str] = []

        warnings.extend(
            f"Resource {resource} in group {group} not found"
            for group, resources in self.config.resource_groups.items()
            for resource in resources
            if resource not in self.config.resources
        )

        warnings.extend(
            f"Processor {processor} in resource {name} not found"
            for name, resource in self.config.resources.items()
            for processor in resource.processors
            if processor.name not in self.config.context_processors
        )

        return warnings

    def _validate_processors(self) -> list[str]:
        """Validate processor configuration.

        Returns:
            List of validation warnings
        """
        warnings = []

        for name, processor in self.config.context_processors.items():
            if processor.type == "function" and not processor.import_path:
                warnings.append(
                    f"Processor {name} missing import_path for type 'function'",
                )
            elif processor.type == "template" and not processor.template:
                warnings.append(
                    f"Processor {name} missing template for type 'template'",
                )

        return warnings

    @logfire.instrument("Validating configs")
    def validate_or_raise(self) -> None:
        """Run all validations and raise on warnings.

        Raises:
            ConfigError: If any validation warnings are found
        """
        warnings = self.validate_all()
        if warnings:
            msg = "Configuration validation failed:\n" + "\n".join(warnings)
            raise exceptions.ConfigError(msg)
