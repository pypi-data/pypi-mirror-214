from typing import List

from importlib_metadata import version
from pydantic import validator
from typing_extensions import override

from dbt_semantic_interfaces.implementations.base import HashableBaseModel
from dbt_semantic_interfaces.implementations.metric import PydanticMetric
from dbt_semantic_interfaces.implementations.semantic_model import PydanticSemanticModel
from dbt_semantic_interfaces.protocols import ProtocolHint, SemanticManifest


class PydanticSemanticManifest(HashableBaseModel, ProtocolHint[SemanticManifest]):
    """Model holds all the information the SemanticLayer needs to render a query."""

    @override
    def _implements_protocol(self) -> SemanticManifest:  # noqa: D
        return self

    semantic_models: List[PydanticSemanticModel]
    metrics: List[PydanticMetric]
    interfaces_version: str = ""

    @validator("interfaces_version", always=True)
    @classmethod
    def __create_default_interfaces_version(cls, value: str) -> str:  # type: ignore[misc]
        """Returns the version of the dbt_semantic_interfaces package that generated this manifest."""
        if value:
            return value
        return version("dbt_semantic_interfaces")
