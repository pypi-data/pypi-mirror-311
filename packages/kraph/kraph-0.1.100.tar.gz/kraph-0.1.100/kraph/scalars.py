import io
from typing import IO, List, Union, Any, Tuple
from graphql import (
    DocumentNode,
    parse,
    OperationDefinitionNode,
    OperationType,
    print_ast,
    print_source_location,
    print_location,
    GraphQLError,
)
from graphql.language.print_location import print_prefixed_lines


class RemoteUpload:
    """A custom scalar for wrapping of every supported array like structure on
    the mikro platform. This scalar enables validation of various array formats
    into a mikro api compliant xr.DataArray.."""

    def __init__(self, value: IO) -> None:
        self.value = value
        self.key = str(value.name)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *info):
        """Validate the input array and convert it to a xr.DataArray."""

        if isinstance(v, str):
            v = open(v, "rb")

        if not isinstance(v, io.IOBase):
            raise ValueError("This needs to be a instance of a file")

        return cls(v)

    def __repr__(self):
        return f"RemoteUpload({self.value})"