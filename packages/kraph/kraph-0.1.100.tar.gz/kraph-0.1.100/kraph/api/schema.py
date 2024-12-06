from kraph.funcs import execute, aexecute
from typing import Any, List, Tuple, Optional, Iterable, Literal
from datetime import datetime
from kraph.traits import (
    GraphTrait,
    LinkedExpressionTrait,
    EntityRelationTrait,
    OntologyTrait,
    ExpressionTrait,
    EntityTrait,
    HasPresignedDownloadAccessor,
)
from enum import Enum
from kraph.rath import KraphRath
from pydantic import BaseModel, ConfigDict, Field
from kraph.scalars import RemoteUpload
from rath.scalars import ID


class ExpressionKind(str, Enum):
    STRUCTURE = "STRUCTURE"
    MEASUREMENT = "MEASUREMENT"
    RELATION = "RELATION"
    ENTITY = "ENTITY"
    METRIC = "METRIC"
    RELATION_METRIC = "RELATION_METRIC"
    CONCEPT = "CONCEPT"


class MetricDataType(str, Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    DATETIME = "DATETIME"
    STRING = "STRING"
    CATEGORY = "CATEGORY"
    BOOLEAN = "BOOLEAN"
    THREE_D_VECTOR = "THREE_D_VECTOR"
    TWO_D_VECTOR = "TWO_D_VECTOR"
    ONE_D_VECTOR = "ONE_D_VECTOR"
    FOUR_D_VECTOR = "FOUR_D_VECTOR"
    N_VECTOR = "N_VECTOR"


class LinkedExpressionFilter(BaseModel):
    graph: Optional[ID] = None
    search: Optional[str] = None
    pinned: Optional[bool] = None
    kind: Optional[ExpressionKind] = None
    ids: Optional[Tuple[ID, ...]] = None
    and_: Optional["LinkedExpressionFilter"] = Field(alias="AND", default=None)
    or_: Optional["LinkedExpressionFilter"] = Field(alias="OR", default=None)
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class OffsetPaginationInput(BaseModel):
    offset: int
    limit: int
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EntityFilter(BaseModel):
    """Filter for entities in the graph"""

    graph: Optional[ID] = None
    "Filter by graph ID"
    kind: Optional[ID] = None
    "Filter by entity kind"
    ids: Optional[Tuple[ID, ...]] = None
    "Filter by list of entity IDs"
    linked_expression: Optional[ID] = Field(alias="linkedExpression", default=None)
    "Filter by linked expression ID"
    identifier: Optional[str] = None
    "Filter by structure identifier"
    object: Optional[ID] = None
    "Filter by associated object ID"
    search: Optional[str] = None
    "Search entities by text"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class GraphPaginationInput(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EntityRelationFilter(BaseModel):
    """Filter for entity relations in the graph"""

    graph: Optional[ID] = None
    "Filter by graph ID"
    kind: Optional[ID] = None
    "Filter by relation kind"
    ids: Optional[Tuple[ID, ...]] = None
    "Filter by list of relation IDs"
    linked_expression: Optional[ID] = Field(alias="linkedExpression", default=None)
    "Filter by linked expression ID"
    search: Optional[str] = None
    "Search relations by text"
    with_self: Optional[bool] = Field(alias="withSelf", default=None)
    "Include self-relations"
    left_id: Optional[ID] = Field(alias="leftId", default=None)
    "Filter by left entity ID"
    right_id: Optional[ID] = Field(alias="rightId", default=None)
    "Filter by right entity ID"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class GraphInput(BaseModel):
    name: str
    experiment: Optional[ID] = None
    description: Optional[str] = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EntityRelationInput(BaseModel):
    """Input type for creating a relation between two entities"""

    left: ID
    "ID of the left entity (format: graph:id)"
    right: ID
    "ID of the right entity (format: graph:id)"
    kind: ID
    "ID of the relation kind (LinkedExpression)"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateEntityMetricInput(BaseModel):
    value: Any
    "The value of the metric."
    entity: ID
    "The entity to attach the metric to."
    metric: ID
    "The metric to attach to the entity."
    timepoint: Optional[datetime] = None
    "The timepoint of the metric."
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateRelationMetricInput(BaseModel):
    value: Any
    relation: ID
    metric: Optional[ID] = None
    timepoint: Optional[datetime] = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructureRelationInput(BaseModel):
    """Input type for creating a relation between two structures"""

    left: "Structure"
    "Left structure of the relation"
    right: "Structure"
    "Right structure of the relation"
    kind: ID
    "ID of the relation kind (LinkedExpression)"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class Structure(BaseModel):
    identifier: str
    id: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ReagentInput(BaseModel):
    lot_id: str = Field(alias="lotId")
    expression: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class MeasurementInput(BaseModel):
    structure: str
    name: Optional[str] = None
    graph: ID
    valid_from: Optional[datetime] = Field(alias="validFrom", default=None)
    valid_to: Optional[datetime] = Field(alias="validTo", default=None)
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ProtocolStepInput(BaseModel):
    """Input type for creating a new protocol step"""

    template: ID
    "ID of the protocol step template"
    entity: ID
    "ID of the entity this step is performed on"
    reagent_mappings: Tuple["ReagentMappingInput", ...] = Field(alias="reagentMappings")
    "List of reagent mappings"
    value_mappings: Tuple["VariableInput", ...] = Field(alias="valueMappings")
    "List of variable mappings"
    performed_at: Optional[datetime] = Field(alias="performedAt", default=None)
    "When the step was performed"
    performed_by: Optional[ID] = Field(alias="performedBy", default=None)
    "ID of the user who performed the step"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ReagentMappingInput(BaseModel):
    """Input type for mapping reagents to protocol steps"""

    reagent: ID
    "ID of the reagent to map"
    volume: int
    "Volume of the reagent in microliters"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class VariableInput(BaseModel):
    """Input type for mapping variables to protocol steps"""

    key: str
    "Key of the variable"
    value: str
    "Value of the variable"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateModelInput(BaseModel):
    """Input type for creating a new model"""

    name: str
    "The name of the model"
    model: RemoteUpload
    "The uploaded model file (e.g. .h5, .onnx, .pt)"
    view: Optional[ID] = None
    "Optional view ID to associate with the model"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RequestMediaUploadInput(BaseModel):
    key: str
    datalayer: str
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EntityInput(BaseModel):
    """Input type for creating a new entity"""

    kind: ID
    "The ID of the kind (LinkedExpression) to create the entity from"
    group: Optional[ID] = None
    "Optional group ID to associate the entity with"
    parent: Optional[ID] = None
    "Optional parent entity ID"
    instance_kind: Optional[str] = Field(alias="instanceKind", default=None)
    "Optional instance kind specification"
    name: Optional[str] = None
    "Optional name for the entity"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class LinkExpressionInput(BaseModel):
    expression: ID
    graph: ID
    color: Optional[Tuple[int, ...]] = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class OntologyInput(BaseModel):
    """Input type for creating a new ontology"""

    name: str
    "The name of the ontology (will be converted to snake_case)"
    description: Optional[str] = None
    "An optional description of the ontology"
    purl: Optional[str] = None
    "An optional PURL (Persistent URL) for the ontology"
    image: Optional[ID] = None
    "An optional ID reference to an associated image"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ExpressionInput(BaseModel):
    """Input for creating a new expression"""

    ontology: Optional[ID] = None
    "The ID of the ontology this expression belongs to. If not provided, uses default ontology"
    label: str
    "The label/name of the expression"
    description: Optional[str] = None
    "A detailed description of the expression"
    purl: Optional[str] = None
    "Permanent URL identifier for the expression"
    color: Optional[Tuple[int, ...]] = None
    "RGBA color values as list of 3 or 4 integers"
    kind: ExpressionKind
    "The kind/type of this expression"
    metric_kind: Optional[MetricDataType] = Field(alias="metricKind", default=None)
    "The type of metric data this expression represents"
    image: Optional[RemoteUpload] = None
    "An optional image associated with this expression"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class LinkedExpressionGraph(GraphTrait, BaseModel):
    """A graph, that contains entities and relations."""

    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class LinkedExpressionExpressionOntology(OntologyTrait, BaseModel):
    """An ontology represents a formal naming and definition of types, properties, and
    interrelationships between entities in a specific domain. In kraph, ontologies provide the vocabulary
    and semantic structure for organizing data across graphs."""

    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    "The unique identifier of the ontology"
    name: str
    "The name of the ontology"
    model_config = ConfigDict(frozen=True)


class LinkedExpressionExpression(ExpressionTrait, BaseModel):
    """An expression in an ontology. Expression are used to label entities and their relations in a graph like structure. Depending on the kind of the expression
    it can be used to describe different aspects of the entities and relations."""

    typename: Literal["Expression"] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    "The unique identifier of the expression."
    label: str
    "The label of the expression. The class"
    ontology: LinkedExpressionExpressionOntology
    "The ontology the expression belongs to."
    model_config = ConfigDict(frozen=True)


class LinkedExpression(LinkedExpressionTrait, BaseModel):
    typename: Literal["LinkedExpression"] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    graph: LinkedExpressionGraph
    kind: ExpressionKind
    expression: LinkedExpressionExpression
    model_config = ConfigDict(frozen=True)


class ListLinkedExpressionGraph(GraphTrait, BaseModel):
    """A graph, that contains entities and relations."""

    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class ListLinkedExpressionExpressionOntology(OntologyTrait, BaseModel):
    """An ontology represents a formal naming and definition of types, properties, and
    interrelationships between entities in a specific domain. In kraph, ontologies provide the vocabulary
    and semantic structure for organizing data across graphs."""

    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    "The unique identifier of the ontology"
    name: str
    "The name of the ontology"
    model_config = ConfigDict(frozen=True)


class ListLinkedExpressionExpression(ExpressionTrait, BaseModel):
    """An expression in an ontology. Expression are used to label entities and their relations in a graph like structure. Depending on the kind of the expression
    it can be used to describe different aspects of the entities and relations."""

    typename: Literal["Expression"] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    "The unique identifier of the expression."
    label: str
    "The label of the expression. The class"
    ontology: ListLinkedExpressionExpressionOntology
    "The ontology the expression belongs to."
    model_config = ConfigDict(frozen=True)


class ListLinkedExpression(LinkedExpressionTrait, BaseModel):
    typename: Literal["LinkedExpression"] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    graph: ListLinkedExpressionGraph
    kind: ExpressionKind
    expression: ListLinkedExpressionExpression
    model_config = ConfigDict(frozen=True)


class PresignedPostCredentials(BaseModel):
    """Temporary Credentials for a file upload that can be used by a Client (e.g. in a python datalayer)"""

    typename: Literal["PresignedPostCredentials"] = Field(
        alias="__typename", default="PresignedPostCredentials", exclude=True
    )
    key: str
    x_amz_credential: str = Field(alias="xAmzCredential")
    x_amz_algorithm: str = Field(alias="xAmzAlgorithm")
    x_amz_date: str = Field(alias="xAmzDate")
    x_amz_signature: str = Field(alias="xAmzSignature")
    policy: str
    datalayer: str
    bucket: str
    store: str
    model_config = ConfigDict(frozen=True)


class Graph(GraphTrait, BaseModel):
    """A graph, that contains entities and relations."""

    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class ProtocolStepTemplate(BaseModel):
    typename: Literal["ProtocolStepTemplate"] = Field(
        alias="__typename", default="ProtocolStepTemplate", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class ProtocolStepReagentmappingsReagent(BaseModel):
    typename: Literal["Reagent"] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class ProtocolStepReagentmappings(BaseModel):
    typename: Literal["ReagentMapping"] = Field(
        alias="__typename", default="ReagentMapping", exclude=True
    )
    reagent: ProtocolStepReagentmappingsReagent
    model_config = ConfigDict(frozen=True)


class ProtocolStepForreagent(BaseModel):
    typename: Literal["Reagent"] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class ProtocolStep(BaseModel):
    typename: Literal["ProtocolStep"] = Field(
        alias="__typename", default="ProtocolStep", exclude=True
    )
    id: ID
    template: ProtocolStepTemplate
    reagent_mappings: Tuple[ProtocolStepReagentmappings, ...] = Field(
        alias="reagentMappings"
    )
    for_reagent: Optional[ProtocolStepForreagent] = Field(
        default=None, alias="forReagent"
    )
    model_config = ConfigDict(frozen=True)


class ExpressionOntology(OntologyTrait, BaseModel):
    """An ontology represents a formal naming and definition of types, properties, and
    interrelationships between entities in a specific domain. In kraph, ontologies provide the vocabulary
    and semantic structure for organizing data across graphs."""

    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    "The unique identifier of the ontology"
    name: str
    "The name of the ontology"
    model_config = ConfigDict(frozen=True)


class Expression(ExpressionTrait, BaseModel):
    """An expression in an ontology. Expression are used to label entities and their relations in a graph like structure. Depending on the kind of the expression
    it can be used to describe different aspects of the entities and relations."""

    typename: Literal["Expression"] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    "The unique identifier of the expression."
    label: str
    "The label of the expression. The class"
    ontology: ExpressionOntology
    "The ontology the expression belongs to."
    model_config = ConfigDict(frozen=True)


class EntityRelationLeft(EntityTrait, BaseModel):
    """An entity is a node in a graph. Entities are the building blocks of the data model in kraph.

    They are used to represent the different objects in your data model, and how they are connected to each other, through
    relations.

    Kraph distinguishes between two core types of entities: Biological entities and Data entities. Biological entities
    are describing real-world objects, such as cells, tissues, organs, etc. Data entities are describing data objects, such as
    images, tables, etc.

    While you can relate any entity to any other entity, it is important to keep in mind that the relations between entities
       should be meaningful, and should reflect the real-world relationships between the objects they represent.

    If you want to attach measurments or metrics to an entity, you should never attach them directly to the entity, but rather
    point from the measurement (the data object) to the entity. This way, you can keep track of the provenance of the data, and
    ensure that you never know anything about the entity that is not backed by data.

    """

    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: ID
    "The unique identifier of the entity within its graph"
    model_config = ConfigDict(frozen=True)


class EntityRelationRight(EntityTrait, BaseModel):
    """An entity is a node in a graph. Entities are the building blocks of the data model in kraph.

    They are used to represent the different objects in your data model, and how they are connected to each other, through
    relations.

    Kraph distinguishes between two core types of entities: Biological entities and Data entities. Biological entities
    are describing real-world objects, such as cells, tissues, organs, etc. Data entities are describing data objects, such as
    images, tables, etc.

    While you can relate any entity to any other entity, it is important to keep in mind that the relations between entities
       should be meaningful, and should reflect the real-world relationships between the objects they represent.

    If you want to attach measurments or metrics to an entity, you should never attach them directly to the entity, but rather
    point from the measurement (the data object) to the entity. This way, you can keep track of the provenance of the data, and
    ensure that you never know anything about the entity that is not backed by data.

    """

    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: ID
    "The unique identifier of the entity within its graph"
    model_config = ConfigDict(frozen=True)


class EntityRelationLinkedexpression(LinkedExpressionTrait, BaseModel):
    typename: Literal["LinkedExpression"] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class EntityRelation(EntityRelationTrait, BaseModel):
    typename: Literal["EntityRelation"] = Field(
        alias="__typename", default="EntityRelation", exclude=True
    )
    id: ID
    left: EntityRelationLeft
    right: EntityRelationRight
    linked_expression: EntityRelationLinkedexpression = Field(alias="linkedExpression")
    model_config = ConfigDict(frozen=True)


class ReagentExpression(ExpressionTrait, BaseModel):
    """An expression in an ontology. Expression are used to label entities and their relations in a graph like structure. Depending on the kind of the expression
    it can be used to describe different aspects of the entities and relations."""

    typename: Literal["Expression"] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    "The unique identifier of the expression."
    model_config = ConfigDict(frozen=True)


class Reagent(BaseModel):
    typename: Literal["Reagent"] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    id: ID
    expression: Optional[ReagentExpression] = Field(default=None)
    lot_id: str = Field(alias="lotId")
    model_config = ConfigDict(frozen=True)


class EntityLinkedexpression(LinkedExpressionTrait, BaseModel):
    typename: Literal["LinkedExpression"] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    label: str
    model_config = ConfigDict(frozen=True)


class Entity(EntityTrait, BaseModel):
    """An entity is a node in a graph. Entities are the building blocks of the data model in kraph.

    They are used to represent the different objects in your data model, and how they are connected to each other, through
    relations.

    Kraph distinguishes between two core types of entities: Biological entities and Data entities. Biological entities
    are describing real-world objects, such as cells, tissues, organs, etc. Data entities are describing data objects, such as
    images, tables, etc.

    While you can relate any entity to any other entity, it is important to keep in mind that the relations between entities
       should be meaningful, and should reflect the real-world relationships between the objects they represent.

    If you want to attach measurments or metrics to an entity, you should never attach them directly to the entity, but rather
    point from the measurement (the data object) to the entity. This way, you can keep track of the provenance of the data, and
    ensure that you never know anything about the entity that is not backed by data.

    """

    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: ID
    "The unique identifier of the entity within its graph"
    label: str
    "A human readable label for this entity"
    linked_expression: EntityLinkedexpression = Field(alias="linkedExpression")
    "The expression that defines this entity's type"
    model_config = ConfigDict(frozen=True)


class ListEntityLinkedexpression(LinkedExpressionTrait, BaseModel):
    typename: Literal["LinkedExpression"] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    label: str
    kind: ExpressionKind
    model_config = ConfigDict(frozen=True)


class ListEntity(EntityTrait, BaseModel):
    """An entity is a node in a graph. Entities are the building blocks of the data model in kraph.

    They are used to represent the different objects in your data model, and how they are connected to each other, through
    relations.

    Kraph distinguishes between two core types of entities: Biological entities and Data entities. Biological entities
    are describing real-world objects, such as cells, tissues, organs, etc. Data entities are describing data objects, such as
    images, tables, etc.

    While you can relate any entity to any other entity, it is important to keep in mind that the relations between entities
       should be meaningful, and should reflect the real-world relationships between the objects they represent.

    If you want to attach measurments or metrics to an entity, you should never attach them directly to the entity, but rather
    point from the measurement (the data object) to the entity. This way, you can keep track of the provenance of the data, and
    ensure that you never know anything about the entity that is not backed by data.

    """

    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: ID
    "The unique identifier of the entity within its graph"
    label: str
    "A human readable label for this entity"
    linked_expression: ListEntityLinkedexpression = Field(alias="linkedExpression")
    "The expression that defines this entity's type"
    object: Optional[str] = Field(default=None)
    "Reference to an external object if this entity represents one"
    identifier: Optional[str] = Field(default=None)
    "A unique identifier for this entity if available"
    model_config = ConfigDict(frozen=True)


class Ontology(OntologyTrait, BaseModel):
    """An ontology represents a formal naming and definition of types, properties, and
    interrelationships between entities in a specific domain. In kraph, ontologies provide the vocabulary
    and semantic structure for organizing data across graphs."""

    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    "The unique identifier of the ontology"
    name: str
    "The name of the ontology"
    model_config = ConfigDict(frozen=True)


class MediaStore(HasPresignedDownloadAccessor, BaseModel):
    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    id: ID
    presigned_url: str = Field(alias="presignedUrl")
    key: str
    model_config = ConfigDict(frozen=True)


class Model(BaseModel):
    """A model represents a trained machine learning model that can be used for analysis."""

    typename: Literal["Model"] = Field(
        alias="__typename", default="Model", exclude=True
    )
    id: ID
    "The unique identifier of the model"
    name: str
    "The name of the model"
    store: Optional[MediaStore] = Field(default=None)
    "Optional file storage location containing the model weights/parameters"
    model_config = ConfigDict(frozen=True)


class LinkExpressionMutation(BaseModel):
    link_expression: LinkedExpression = Field(alias="linkExpression")
    "Link an expression to an entity"

    class Arguments(BaseModel):
        input: LinkExpressionInput

    class Meta:
        document = "fragment LinkedExpression on LinkedExpression {\n  id\n  graph {\n    id\n    __typename\n  }\n  kind\n  expression {\n    id\n    label\n    ontology {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nmutation LinkExpression($input: LinkExpressionInput!) {\n  linkExpression(input: $input) {\n    ...LinkedExpression\n    __typename\n  }\n}"


class CreateModelMutation(BaseModel):
    create_model: Model = Field(alias="createModel")
    "Create a new model"

    class Arguments(BaseModel):
        input: CreateModelInput

    class Meta:
        document = "fragment MediaStore on MediaStore {\n  id\n  presignedUrl\n  key\n  __typename\n}\n\nfragment Model on Model {\n  id\n  name\n  store {\n    ...MediaStore\n    __typename\n  }\n  __typename\n}\n\nmutation CreateModel($input: CreateModelInput!) {\n  createModel(input: $input) {\n    ...Model\n    __typename\n  }\n}"


class CreateGraphMutation(BaseModel):
    create_graph: Graph = Field(alias="createGraph")
    "Create a new graph"

    class Arguments(BaseModel):
        input: GraphInput

    class Meta:
        document = "fragment Graph on Graph {\n  id\n  name\n  __typename\n}\n\nmutation CreateGraph($input: GraphInput!) {\n  createGraph(input: $input) {\n    ...Graph\n    __typename\n  }\n}"


class RequestUploadMutation(BaseModel):
    request_upload: PresignedPostCredentials = Field(alias="requestUpload")
    "Request a new file upload"

    class Arguments(BaseModel):
        input: RequestMediaUploadInput

    class Meta:
        document = "fragment PresignedPostCredentials on PresignedPostCredentials {\n  key\n  xAmzCredential\n  xAmzAlgorithm\n  xAmzDate\n  xAmzSignature\n  policy\n  datalayer\n  bucket\n  store\n  __typename\n}\n\nmutation RequestUpload($input: RequestMediaUploadInput!) {\n  requestUpload(input: $input) {\n    ...PresignedPostCredentials\n    __typename\n  }\n}"


class CreateProtocolStepMutation(BaseModel):
    create_protocol_step: ProtocolStep = Field(alias="createProtocolStep")
    "Create a new protocol step"

    class Arguments(BaseModel):
        input: ProtocolStepInput

    class Meta:
        document = "fragment ProtocolStep on ProtocolStep {\n  id\n  template {\n    id\n    name\n    __typename\n  }\n  reagentMappings {\n    reagent {\n      id\n      __typename\n    }\n    __typename\n  }\n  forReagent {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation CreateProtocolStep($input: ProtocolStepInput!) {\n  createProtocolStep(input: $input) {\n    ...ProtocolStep\n    __typename\n  }\n}"


class CreateExpressionMutation(BaseModel):
    create_expression: Expression = Field(alias="createExpression")
    "Create a new expression"

    class Arguments(BaseModel):
        input: ExpressionInput

    class Meta:
        document = "fragment Expression on Expression {\n  id\n  label\n  ontology {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nmutation CreateExpression($input: ExpressionInput!) {\n  createExpression(input: $input) {\n    ...Expression\n    __typename\n  }\n}"


class CreateEntityRelationMutation(BaseModel):
    create_entity_relation: EntityRelation = Field(alias="createEntityRelation")
    "Create a new relation between entities"

    class Arguments(BaseModel):
        input: EntityRelationInput

    class Meta:
        document = "fragment EntityRelation on EntityRelation {\n  id\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  linkedExpression {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation CreateEntityRelation($input: EntityRelationInput!) {\n  createEntityRelation(input: $input) {\n    ...EntityRelation\n    __typename\n  }\n}"


class CreateRoiEntityRelationMutation(BaseModel):
    create_structure_relation: EntityRelation = Field(alias="createStructureRelation")
    "Create a relation between structures"

    class Arguments(BaseModel):
        input: StructureRelationInput

    class Meta:
        document = "fragment EntityRelation on EntityRelation {\n  id\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  linkedExpression {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation CreateRoiEntityRelation($input: StructureRelationInput!) {\n  createStructureRelation(input: $input) {\n    ...EntityRelation\n    __typename\n  }\n}"


class CreateReagentMutation(BaseModel):
    create_reagent: Reagent = Field(alias="createReagent")
    "Create a new reagent"

    class Arguments(BaseModel):
        input: ReagentInput

    class Meta:
        document = "fragment Reagent on Reagent {\n  id\n  expression {\n    id\n    __typename\n  }\n  lotId\n  __typename\n}\n\nmutation CreateReagent($input: ReagentInput!) {\n  createReagent(input: $input) {\n    ...Reagent\n    __typename\n  }\n}"


class CreateEntityMetricMutation(BaseModel):
    create_entity_metric: Entity = Field(alias="createEntityMetric")
    "Create a new metric for an entity"

    class Arguments(BaseModel):
        input: CreateEntityMetricInput

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nmutation CreateEntityMetric($input: CreateEntityMetricInput!) {\n  createEntityMetric(input: $input) {\n    ...Entity\n    __typename\n  }\n}"


class CreateRelationMetricMutation(BaseModel):
    create_relation_metric: EntityRelation = Field(alias="createRelationMetric")
    "Create a new metric for a relation"

    class Arguments(BaseModel):
        input: CreateRelationMetricInput

    class Meta:
        document = "fragment EntityRelation on EntityRelation {\n  id\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  linkedExpression {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation CreateRelationMetric($input: CreateRelationMetricInput!) {\n  createRelationMetric(input: $input) {\n    ...EntityRelation\n    __typename\n  }\n}"


class CreateEntityMutation(BaseModel):
    create_entity: Entity = Field(alias="createEntity")
    "Create a new entity"

    class Arguments(BaseModel):
        input: EntityInput

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nmutation CreateEntity($input: EntityInput!) {\n  createEntity(input: $input) {\n    ...Entity\n    __typename\n  }\n}"


class CreateMeasurementMutation(BaseModel):
    create_measurement: Entity = Field(alias="createMeasurement")
    "Create a new measurement"

    class Arguments(BaseModel):
        input: MeasurementInput

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nmutation CreateMeasurement($input: MeasurementInput!) {\n  createMeasurement(input: $input) {\n    ...Entity\n    __typename\n  }\n}"


class CreateOntologyMutation(BaseModel):
    create_ontology: Ontology = Field(alias="createOntology")
    "Create a new ontology"

    class Arguments(BaseModel):
        input: OntologyInput

    class Meta:
        document = "fragment Ontology on Ontology {\n  id\n  name\n  __typename\n}\n\nmutation CreateOntology($input: OntologyInput!) {\n  createOntology(input: $input) {\n    ...Ontology\n    __typename\n  }\n}"


class GetLinkedExpressionQuery(BaseModel):
    linked_expression: LinkedExpression = Field(alias="linkedExpression")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment LinkedExpression on LinkedExpression {\n  id\n  graph {\n    id\n    __typename\n  }\n  kind\n  expression {\n    id\n    label\n    ontology {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery GetLinkedExpression($id: ID!) {\n  linkedExpression(id: $id) {\n    ...LinkedExpression\n    __typename\n  }\n}"


class SearchLinkedExpressionsQueryOptions(LinkedExpressionTrait, BaseModel):
    typename: Literal["LinkedExpression"] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchLinkedExpressionsQuery(BaseModel):
    options: Tuple[SearchLinkedExpressionsQueryOptions, ...]
    "List of all expressions that are linked in a Graph"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchLinkedExpressions($search: String, $values: [ID!]) {\n  options: linkedExpressions(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class ListLinkedExpressionsQuery(BaseModel):
    linked_expressions: Tuple[ListLinkedExpression, ...] = Field(
        alias="linkedExpressions"
    )
    "List of all expressions that are linked in a Graph"

    class Arguments(BaseModel):
        filters: Optional[LinkedExpressionFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)

    class Meta:
        document = "fragment ListLinkedExpression on LinkedExpression {\n  id\n  graph {\n    id\n    __typename\n  }\n  kind\n  expression {\n    id\n    label\n    ontology {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery ListLinkedExpressions($filters: LinkedExpressionFilter, $pagination: OffsetPaginationInput) {\n  linkedExpressions(filters: $filters, pagination: $pagination) {\n    ...ListLinkedExpression\n    __typename\n  }\n}"


class GetModelQuery(BaseModel):
    model: Model

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment MediaStore on MediaStore {\n  id\n  presignedUrl\n  key\n  __typename\n}\n\nfragment Model on Model {\n  id\n  name\n  store {\n    ...MediaStore\n    __typename\n  }\n  __typename\n}\n\nquery GetModel($id: ID!) {\n  model(id: $id) {\n    ...Model\n    __typename\n  }\n}"


class SearchModelsQueryOptions(BaseModel):
    """A model represents a trained machine learning model that can be used for analysis."""

    typename: Literal["Model"] = Field(
        alias="__typename", default="Model", exclude=True
    )
    value: ID
    "The unique identifier of the model"
    label: str
    "The name of the model"
    model_config = ConfigDict(frozen=True)


class SearchModelsQuery(BaseModel):
    options: Tuple[SearchModelsQueryOptions, ...]
    "List of all deep learning models (e.g. neural networks)"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchModels($search: String, $values: [ID!]) {\n  options: models(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class GetGraphQuery(BaseModel):
    graph: Graph

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Graph on Graph {\n  id\n  name\n  __typename\n}\n\nquery GetGraph($id: ID!) {\n  graph(id: $id) {\n    ...Graph\n    __typename\n  }\n}"


class SearchGraphsQueryOptions(GraphTrait, BaseModel):
    """A graph, that contains entities and relations."""

    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchGraphsQuery(BaseModel):
    options: Tuple[SearchGraphsQueryOptions, ...]
    "List of all knowledge graphs"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchGraphs($search: String, $values: [ID!]) {\n  options: graphs(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class GetProtocolStepQuery(BaseModel):
    protocol_step: ProtocolStep = Field(alias="protocolStep")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment ProtocolStep on ProtocolStep {\n  id\n  template {\n    id\n    name\n    __typename\n  }\n  reagentMappings {\n    reagent {\n      id\n      __typename\n    }\n    __typename\n  }\n  forReagent {\n    id\n    __typename\n  }\n  __typename\n}\n\nquery GetProtocolStep($id: ID!) {\n  protocolStep(id: $id) {\n    ...ProtocolStep\n    __typename\n  }\n}"


class SearchProtocolStepsQueryOptions(BaseModel):
    typename: Literal["ProtocolStep"] = Field(
        alias="__typename", default="ProtocolStep", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchProtocolStepsQuery(BaseModel):
    options: Tuple[SearchProtocolStepsQueryOptions, ...]
    "List of all protocol steps"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchProtocolSteps($search: String, $values: [ID!]) {\n  options: protocolSteps(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class GetEntityRelationQuery(BaseModel):
    entity_relation: EntityRelation = Field(alias="entityRelation")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment EntityRelation on EntityRelation {\n  id\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  linkedExpression {\n    id\n    __typename\n  }\n  __typename\n}\n\nquery GetEntityRelation($id: ID!) {\n  entityRelation(id: $id) {\n    ...EntityRelation\n    __typename\n  }\n}"


class SearchEntityRelationsQueryOptions(EntityRelationTrait, BaseModel):
    typename: Literal["EntityRelation"] = Field(
        alias="__typename", default="EntityRelation", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchEntityRelationsQuery(BaseModel):
    options: Tuple[SearchEntityRelationsQueryOptions, ...]
    "List of all relationships between entities"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchEntityRelations($search: String, $values: [ID!]) {\n  options: entityRelations(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetReagentQuery(BaseModel):
    reagent: Reagent

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Reagent on Reagent {\n  id\n  expression {\n    id\n    __typename\n  }\n  lotId\n  __typename\n}\n\nquery GetReagent($id: ID!) {\n  reagent(id: $id) {\n    ...Reagent\n    __typename\n  }\n}"


class SearchReagentsQueryOptions(BaseModel):
    typename: Literal["Reagent"] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchReagentsQuery(BaseModel):
    options: Tuple[SearchReagentsQueryOptions, ...]
    "List of all reagents used in protocols"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchReagents($search: String, $values: [ID!]) {\n  options: reagents(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetEntityQuery(BaseModel):
    entity: Entity

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nquery GetEntity($id: ID!) {\n  entity(id: $id) {\n    ...Entity\n    __typename\n  }\n}"


class SearchEntitiesQueryOptions(EntityTrait, BaseModel):
    """An entity is a node in a graph. Entities are the building blocks of the data model in kraph.

    They are used to represent the different objects in your data model, and how they are connected to each other, through
    relations.

    Kraph distinguishes between two core types of entities: Biological entities and Data entities. Biological entities
    are describing real-world objects, such as cells, tissues, organs, etc. Data entities are describing data objects, such as
    images, tables, etc.

    While you can relate any entity to any other entity, it is important to keep in mind that the relations between entities
       should be meaningful, and should reflect the real-world relationships between the objects they represent.

    If you want to attach measurments or metrics to an entity, you should never attach them directly to the entity, but rather
    point from the measurement (the data object) to the entity. This way, you can keep track of the provenance of the data, and
    ensure that you never know anything about the entity that is not backed by data.

    """

    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    value: ID
    "The unique identifier of the entity within its graph"
    label: str
    "A human readable label for this entity"
    model_config = ConfigDict(frozen=True)


class SearchEntitiesQuery(BaseModel):
    options: Tuple[SearchEntitiesQueryOptions, ...]
    "List of all entities in the system"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchEntities($search: String, $values: [ID!]) {\n  options: entities(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class EntitiesQuery(BaseModel):
    entities: Tuple[Entity, ...]
    "List of all entities in the system"

    class Arguments(BaseModel):
        filters: Optional[EntityFilter] = Field(default=None)
        pagination: Optional[GraphPaginationInput] = Field(default=None)

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nquery Entities($filters: EntityFilter, $pagination: GraphPaginationInput) {\n  entities(filters: $filters, pagination: $pagination) {\n    ...Entity\n    __typename\n  }\n}"


class ListPairedEntitiesQueryPairedentitiesRelation(EntityRelationTrait, BaseModel):
    typename: Literal["EntityRelation"] = Field(
        alias="__typename", default="EntityRelation", exclude=True
    )
    id: ID
    label: str
    model_config = ConfigDict(frozen=True)


class ListPairedEntitiesQueryPairedentities(BaseModel):
    """A paired structure two entities and the relation between them."""

    typename: Literal["PairedStructure"] = Field(
        alias="__typename", default="PairedStructure", exclude=True
    )
    left: ListEntity
    "The left entity."
    right: ListEntity
    "The right entity."
    relation: ListPairedEntitiesQueryPairedentitiesRelation
    "The relation between the two entities."
    model_config = ConfigDict(frozen=True)


class ListPairedEntitiesQuery(BaseModel):
    paired_entities: Tuple[ListPairedEntitiesQueryPairedentities, ...] = Field(
        alias="pairedEntities"
    )
    "Retrieves paired entities"

    class Arguments(BaseModel):
        graph: ID
        relation_filter: Optional[EntityRelationFilter] = Field(
            alias="relationFilter", default=None
        )
        left_filter: Optional[EntityFilter] = Field(alias="leftFilter", default=None)
        right_filter: Optional[EntityFilter] = Field(alias="rightFilter", default=None)
        pagination: Optional[GraphPaginationInput] = Field(default=None)

    class Meta:
        document = "fragment ListEntity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n    kind\n    __typename\n  }\n  object\n  identifier\n  __typename\n}\n\nquery ListPairedEntities($graph: ID!, $relationFilter: EntityRelationFilter, $leftFilter: EntityFilter, $rightFilter: EntityFilter, $pagination: GraphPaginationInput) {\n  pairedEntities(\n    graph: $graph\n    rightFilter: $rightFilter\n    pagination: $pagination\n    leftFilter: $leftFilter\n    relationFilter: $relationFilter\n  ) {\n    left {\n      ...ListEntity\n      __typename\n    }\n    right {\n      ...ListEntity\n      __typename\n    }\n    relation {\n      id\n      label\n      __typename\n    }\n    __typename\n  }\n}"


class GetOntologyQuery(BaseModel):
    ontology: Ontology

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Ontology on Ontology {\n  id\n  name\n  __typename\n}\n\nquery GetOntology($id: ID!) {\n  ontology(id: $id) {\n    ...Ontology\n    __typename\n  }\n}"


class SearchOntologiesQueryOptions(OntologyTrait, BaseModel):
    """An ontology represents a formal naming and definition of types, properties, and
    interrelationships between entities in a specific domain. In kraph, ontologies provide the vocabulary
    and semantic structure for organizing data across graphs."""

    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    value: ID
    "The unique identifier of the ontology"
    label: str
    "The name of the ontology"
    model_config = ConfigDict(frozen=True)


class SearchOntologiesQuery(BaseModel):
    options: Tuple[SearchOntologiesQueryOptions, ...]
    "List of all ontologies"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchOntologies($search: String, $values: [ID!]) {\n  options: ontologies(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


async def alink_expression(
    expression: ID,
    graph: ID,
    color: Optional[Iterable[int]] = None,
    rath: Optional[KraphRath] = None,
) -> LinkedExpression:
    """LinkExpression

    Link an expression to an entity

    Arguments:
        expression: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        graph: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        color: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        LinkedExpression"""
    return (
        await aexecute(
            LinkExpressionMutation,
            {"input": {"expression": expression, "graph": graph, "color": color}},
            rath=rath,
        )
    ).link_expression


def link_expression(
    expression: ID,
    graph: ID,
    color: Optional[Iterable[int]] = None,
    rath: Optional[KraphRath] = None,
) -> LinkedExpression:
    """LinkExpression

    Link an expression to an entity

    Arguments:
        expression: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        graph: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        color: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        LinkedExpression"""
    return execute(
        LinkExpressionMutation,
        {"input": {"expression": expression, "graph": graph, "color": color}},
        rath=rath,
    ).link_expression


async def acreate_model(
    name: str,
    model: RemoteUpload,
    view: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> Model:
    """CreateModel

    Create a new model

    Arguments:
        name: The name of the model
        model: The uploaded model file (e.g. .h5, .onnx, .pt)
        view: Optional view ID to associate with the model
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Model"""
    return (
        await aexecute(
            CreateModelMutation,
            {"input": {"name": name, "model": model, "view": view}},
            rath=rath,
        )
    ).create_model


def create_model(
    name: str,
    model: RemoteUpload,
    view: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> Model:
    """CreateModel

    Create a new model

    Arguments:
        name: The name of the model
        model: The uploaded model file (e.g. .h5, .onnx, .pt)
        view: Optional view ID to associate with the model
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Model"""
    return execute(
        CreateModelMutation,
        {"input": {"name": name, "model": model, "view": view}},
        rath=rath,
    ).create_model


async def acreate_graph(
    name: str,
    experiment: Optional[ID] = None,
    description: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Graph:
    """CreateGraph

    Create a new graph

    Arguments:
        name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        experiment: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
        description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Graph"""
    return (
        await aexecute(
            CreateGraphMutation,
            {
                "input": {
                    "name": name,
                    "experiment": experiment,
                    "description": description,
                }
            },
            rath=rath,
        )
    ).create_graph


def create_graph(
    name: str,
    experiment: Optional[ID] = None,
    description: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Graph:
    """CreateGraph

    Create a new graph

    Arguments:
        name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        experiment: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
        description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Graph"""
    return execute(
        CreateGraphMutation,
        {"input": {"name": name, "experiment": experiment, "description": description}},
        rath=rath,
    ).create_graph


async def arequest_upload(
    key: str, datalayer: str, rath: Optional[KraphRath] = None
) -> PresignedPostCredentials:
    """RequestUpload

    Request a new file upload

    Arguments:
        key: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        datalayer: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        PresignedPostCredentials"""
    return (
        await aexecute(
            RequestUploadMutation,
            {"input": {"key": key, "datalayer": datalayer}},
            rath=rath,
        )
    ).request_upload


def request_upload(
    key: str, datalayer: str, rath: Optional[KraphRath] = None
) -> PresignedPostCredentials:
    """RequestUpload

    Request a new file upload

    Arguments:
        key: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        datalayer: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        PresignedPostCredentials"""
    return execute(
        RequestUploadMutation,
        {"input": {"key": key, "datalayer": datalayer}},
        rath=rath,
    ).request_upload


async def acreate_protocol_step(
    template: ID,
    entity: ID,
    reagent_mappings: Iterable[ReagentMappingInput],
    value_mappings: Iterable[VariableInput],
    performed_at: Optional[datetime] = None,
    performed_by: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> ProtocolStep:
    """CreateProtocolStep

    Create a new protocol step

    Arguments:
        template: ID of the protocol step template
        entity: ID of the entity this step is performed on
        reagent_mappings: List of reagent mappings
        value_mappings: List of variable mappings
        performed_at: When the step was performed
        performed_by: ID of the user who performed the step
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ProtocolStep"""
    return (
        await aexecute(
            CreateProtocolStepMutation,
            {
                "input": {
                    "template": template,
                    "entity": entity,
                    "reagent_mappings": reagent_mappings,
                    "value_mappings": value_mappings,
                    "performed_at": performed_at,
                    "performed_by": performed_by,
                }
            },
            rath=rath,
        )
    ).create_protocol_step


def create_protocol_step(
    template: ID,
    entity: ID,
    reagent_mappings: Iterable[ReagentMappingInput],
    value_mappings: Iterable[VariableInput],
    performed_at: Optional[datetime] = None,
    performed_by: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> ProtocolStep:
    """CreateProtocolStep

    Create a new protocol step

    Arguments:
        template: ID of the protocol step template
        entity: ID of the entity this step is performed on
        reagent_mappings: List of reagent mappings
        value_mappings: List of variable mappings
        performed_at: When the step was performed
        performed_by: ID of the user who performed the step
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ProtocolStep"""
    return execute(
        CreateProtocolStepMutation,
        {
            "input": {
                "template": template,
                "entity": entity,
                "reagent_mappings": reagent_mappings,
                "value_mappings": value_mappings,
                "performed_at": performed_at,
                "performed_by": performed_by,
            }
        },
        rath=rath,
    ).create_protocol_step


async def acreate_expression(
    label: str,
    kind: ExpressionKind,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    color: Optional[Iterable[int]] = None,
    metric_kind: Optional[MetricDataType] = None,
    image: Optional[RemoteUpload] = None,
    rath: Optional[KraphRath] = None,
) -> Expression:
    """CreateExpression

    Create a new expression

    Arguments:
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        label: The label/name of the expression
        description: A detailed description of the expression
        purl: Permanent URL identifier for the expression
        color: RGBA color values as list of 3 or 4 integers
        kind: The kind/type of this expression
        metric_kind: The type of metric data this expression represents
        image: An optional image associated with this expression
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Expression"""
    return (
        await aexecute(
            CreateExpressionMutation,
            {
                "input": {
                    "ontology": ontology,
                    "label": label,
                    "description": description,
                    "purl": purl,
                    "color": color,
                    "kind": kind,
                    "metric_kind": metric_kind,
                    "image": image,
                }
            },
            rath=rath,
        )
    ).create_expression


def create_expression(
    label: str,
    kind: ExpressionKind,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    color: Optional[Iterable[int]] = None,
    metric_kind: Optional[MetricDataType] = None,
    image: Optional[RemoteUpload] = None,
    rath: Optional[KraphRath] = None,
) -> Expression:
    """CreateExpression

    Create a new expression

    Arguments:
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        label: The label/name of the expression
        description: A detailed description of the expression
        purl: Permanent URL identifier for the expression
        color: RGBA color values as list of 3 or 4 integers
        kind: The kind/type of this expression
        metric_kind: The type of metric data this expression represents
        image: An optional image associated with this expression
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Expression"""
    return execute(
        CreateExpressionMutation,
        {
            "input": {
                "ontology": ontology,
                "label": label,
                "description": description,
                "purl": purl,
                "color": color,
                "kind": kind,
                "metric_kind": metric_kind,
                "image": image,
            }
        },
        rath=rath,
    ).create_expression


async def acreate_entity_relation(
    left: ID, right: ID, kind: ID, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """CreateEntityRelation

    Create a new relation between entities

    Arguments:
        left: ID of the left entity (format: graph:id)
        right: ID of the right entity (format: graph:id)
        kind: ID of the relation kind (LinkedExpression)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return (
        await aexecute(
            CreateEntityRelationMutation,
            {"input": {"left": left, "right": right, "kind": kind}},
            rath=rath,
        )
    ).create_entity_relation


def create_entity_relation(
    left: ID, right: ID, kind: ID, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """CreateEntityRelation

    Create a new relation between entities

    Arguments:
        left: ID of the left entity (format: graph:id)
        right: ID of the right entity (format: graph:id)
        kind: ID of the relation kind (LinkedExpression)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return execute(
        CreateEntityRelationMutation,
        {"input": {"left": left, "right": right, "kind": kind}},
        rath=rath,
    ).create_entity_relation


async def acreate_roi_entity_relation(
    left: Structure, right: Structure, kind: ID, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """CreateRoiEntityRelation

    Create a relation between structures

    Arguments:
        left: Left structure of the relation
        right: Right structure of the relation
        kind: ID of the relation kind (LinkedExpression)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return (
        await aexecute(
            CreateRoiEntityRelationMutation,
            {"input": {"left": left, "right": right, "kind": kind}},
            rath=rath,
        )
    ).create_structure_relation


def create_roi_entity_relation(
    left: Structure, right: Structure, kind: ID, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """CreateRoiEntityRelation

    Create a relation between structures

    Arguments:
        left: Left structure of the relation
        right: Right structure of the relation
        kind: ID of the relation kind (LinkedExpression)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return execute(
        CreateRoiEntityRelationMutation,
        {"input": {"left": left, "right": right, "kind": kind}},
        rath=rath,
    ).create_structure_relation


async def acreate_reagent(
    lot_id: str, expression: ID, rath: Optional[KraphRath] = None
) -> Reagent:
    """CreateReagent

    Create a new reagent

    Arguments:
        lot_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        expression: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Reagent"""
    return (
        await aexecute(
            CreateReagentMutation,
            {"input": {"lot_id": lot_id, "expression": expression}},
            rath=rath,
        )
    ).create_reagent


def create_reagent(
    lot_id: str, expression: ID, rath: Optional[KraphRath] = None
) -> Reagent:
    """CreateReagent

    Create a new reagent

    Arguments:
        lot_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        expression: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Reagent"""
    return execute(
        CreateReagentMutation,
        {"input": {"lot_id": lot_id, "expression": expression}},
        rath=rath,
    ).create_reagent


async def acreate_entity_metric(
    value: Any,
    entity: ID,
    metric: ID,
    timepoint: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntityMetric

    Create a new metric for an entity

    Arguments:
        value: The value of the metric.
        entity: The entity to attach the metric to.
        metric: The metric to attach to the entity.
        timepoint: The timepoint of the metric.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return (
        await aexecute(
            CreateEntityMetricMutation,
            {
                "input": {
                    "value": value,
                    "entity": entity,
                    "metric": metric,
                    "timepoint": timepoint,
                }
            },
            rath=rath,
        )
    ).create_entity_metric


def create_entity_metric(
    value: Any,
    entity: ID,
    metric: ID,
    timepoint: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntityMetric

    Create a new metric for an entity

    Arguments:
        value: The value of the metric.
        entity: The entity to attach the metric to.
        metric: The metric to attach to the entity.
        timepoint: The timepoint of the metric.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return execute(
        CreateEntityMetricMutation,
        {
            "input": {
                "value": value,
                "entity": entity,
                "metric": metric,
                "timepoint": timepoint,
            }
        },
        rath=rath,
    ).create_entity_metric


async def acreate_relation_metric(
    value: Any,
    relation: ID,
    metric: Optional[ID] = None,
    timepoint: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> EntityRelation:
    """CreateRelationMetric

    Create a new metric for a relation

    Arguments:
        value: The `Metric` scalar type represents a matrix values as specified by (required)
        relation: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        metric: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
        timepoint: Date with time (isoformat)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return (
        await aexecute(
            CreateRelationMetricMutation,
            {
                "input": {
                    "value": value,
                    "relation": relation,
                    "metric": metric,
                    "timepoint": timepoint,
                }
            },
            rath=rath,
        )
    ).create_relation_metric


def create_relation_metric(
    value: Any,
    relation: ID,
    metric: Optional[ID] = None,
    timepoint: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> EntityRelation:
    """CreateRelationMetric

    Create a new metric for a relation

    Arguments:
        value: The `Metric` scalar type represents a matrix values as specified by (required)
        relation: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        metric: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
        timepoint: Date with time (isoformat)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return execute(
        CreateRelationMetricMutation,
        {
            "input": {
                "value": value,
                "relation": relation,
                "metric": metric,
                "timepoint": timepoint,
            }
        },
        rath=rath,
    ).create_relation_metric


async def acreate_entity(
    kind: ID,
    group: Optional[ID] = None,
    parent: Optional[ID] = None,
    instance_kind: Optional[str] = None,
    name: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntity

    Create a new entity

    Arguments:
        kind: The ID of the kind (LinkedExpression) to create the entity from
        group: Optional group ID to associate the entity with
        parent: Optional parent entity ID
        instance_kind: Optional instance kind specification
        name: Optional name for the entity
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return (
        await aexecute(
            CreateEntityMutation,
            {
                "input": {
                    "kind": kind,
                    "group": group,
                    "parent": parent,
                    "instance_kind": instance_kind,
                    "name": name,
                }
            },
            rath=rath,
        )
    ).create_entity


def create_entity(
    kind: ID,
    group: Optional[ID] = None,
    parent: Optional[ID] = None,
    instance_kind: Optional[str] = None,
    name: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntity

    Create a new entity

    Arguments:
        kind: The ID of the kind (LinkedExpression) to create the entity from
        group: Optional group ID to associate the entity with
        parent: Optional parent entity ID
        instance_kind: Optional instance kind specification
        name: Optional name for the entity
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return execute(
        CreateEntityMutation,
        {
            "input": {
                "kind": kind,
                "group": group,
                "parent": parent,
                "instance_kind": instance_kind,
                "name": name,
            }
        },
        rath=rath,
    ).create_entity


async def acreate_measurement(
    structure: str,
    graph: ID,
    name: Optional[str] = None,
    valid_from: Optional[datetime] = None,
    valid_to: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateMeasurement

    Create a new measurement

    Arguments:
        structure: The `StructureString` scalar type represents a string with a structure (required)
        name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
        graph: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        valid_from: Date with time (isoformat)
        valid_to: Date with time (isoformat)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return (
        await aexecute(
            CreateMeasurementMutation,
            {
                "input": {
                    "structure": structure,
                    "name": name,
                    "graph": graph,
                    "valid_from": valid_from,
                    "valid_to": valid_to,
                }
            },
            rath=rath,
        )
    ).create_measurement


def create_measurement(
    structure: str,
    graph: ID,
    name: Optional[str] = None,
    valid_from: Optional[datetime] = None,
    valid_to: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateMeasurement

    Create a new measurement

    Arguments:
        structure: The `StructureString` scalar type represents a string with a structure (required)
        name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
        graph: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        valid_from: Date with time (isoformat)
        valid_to: Date with time (isoformat)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return execute(
        CreateMeasurementMutation,
        {
            "input": {
                "structure": structure,
                "name": name,
                "graph": graph,
                "valid_from": valid_from,
                "valid_to": valid_to,
            }
        },
        rath=rath,
    ).create_measurement


async def acreate_ontology(
    name: str,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    image: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> Ontology:
    """CreateOntology

    Create a new ontology

    Arguments:
        name: The name of the ontology (will be converted to snake_case)
        description: An optional description of the ontology
        purl: An optional PURL (Persistent URL) for the ontology
        image: An optional ID reference to an associated image
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Ontology"""
    return (
        await aexecute(
            CreateOntologyMutation,
            {
                "input": {
                    "name": name,
                    "description": description,
                    "purl": purl,
                    "image": image,
                }
            },
            rath=rath,
        )
    ).create_ontology


def create_ontology(
    name: str,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    image: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> Ontology:
    """CreateOntology

    Create a new ontology

    Arguments:
        name: The name of the ontology (will be converted to snake_case)
        description: An optional description of the ontology
        purl: An optional PURL (Persistent URL) for the ontology
        image: An optional ID reference to an associated image
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Ontology"""
    return execute(
        CreateOntologyMutation,
        {
            "input": {
                "name": name,
                "description": description,
                "purl": purl,
                "image": image,
            }
        },
        rath=rath,
    ).create_ontology


async def aget_linked_expression(
    id: ID, rath: Optional[KraphRath] = None
) -> LinkedExpression:
    """GetLinkedExpression


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        LinkedExpression"""
    return (
        await aexecute(GetLinkedExpressionQuery, {"id": id}, rath=rath)
    ).linked_expression


def get_linked_expression(id: ID, rath: Optional[KraphRath] = None) -> LinkedExpression:
    """GetLinkedExpression


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        LinkedExpression"""
    return execute(GetLinkedExpressionQuery, {"id": id}, rath=rath).linked_expression


async def asearch_linked_expressions(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchLinkedExpressionsQueryOptions]:
    """SearchLinkedExpressions

    List of all expressions that are linked in a Graph

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchLinkedExpressionsQueryLinkedexpressions]"""
    return (
        await aexecute(
            SearchLinkedExpressionsQuery,
            {"search": search, "values": values},
            rath=rath,
        )
    ).options


def search_linked_expressions(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchLinkedExpressionsQueryOptions]:
    """SearchLinkedExpressions

    List of all expressions that are linked in a Graph

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchLinkedExpressionsQueryLinkedexpressions]"""
    return execute(
        SearchLinkedExpressionsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def alist_linked_expressions(
    filters: Optional[LinkedExpressionFilter] = None,
    pagination: Optional[OffsetPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[ListLinkedExpression]:
    """ListLinkedExpressions

    List of all expressions that are linked in a Graph

    Arguments:
        filters (Optional[LinkedExpressionFilter], optional): No description.
        pagination (Optional[OffsetPaginationInput], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[ListLinkedExpression]"""
    return (
        await aexecute(
            ListLinkedExpressionsQuery,
            {"filters": filters, "pagination": pagination},
            rath=rath,
        )
    ).linked_expressions


def list_linked_expressions(
    filters: Optional[LinkedExpressionFilter] = None,
    pagination: Optional[OffsetPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[ListLinkedExpression]:
    """ListLinkedExpressions

    List of all expressions that are linked in a Graph

    Arguments:
        filters (Optional[LinkedExpressionFilter], optional): No description.
        pagination (Optional[OffsetPaginationInput], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[ListLinkedExpression]"""
    return execute(
        ListLinkedExpressionsQuery,
        {"filters": filters, "pagination": pagination},
        rath=rath,
    ).linked_expressions


async def aget_model(id: ID, rath: Optional[KraphRath] = None) -> Model:
    """GetModel


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Model"""
    return (await aexecute(GetModelQuery, {"id": id}, rath=rath)).model


def get_model(id: ID, rath: Optional[KraphRath] = None) -> Model:
    """GetModel


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Model"""
    return execute(GetModelQuery, {"id": id}, rath=rath).model


async def asearch_models(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchModelsQueryOptions]:
    """SearchModels

    List of all deep learning models (e.g. neural networks)

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchModelsQueryModels]"""
    return (
        await aexecute(
            SearchModelsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_models(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchModelsQueryOptions]:
    """SearchModels

    List of all deep learning models (e.g. neural networks)

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchModelsQueryModels]"""
    return execute(
        SearchModelsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_graph(id: ID, rath: Optional[KraphRath] = None) -> Graph:
    """GetGraph


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Graph"""
    return (await aexecute(GetGraphQuery, {"id": id}, rath=rath)).graph


def get_graph(id: ID, rath: Optional[KraphRath] = None) -> Graph:
    """GetGraph


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Graph"""
    return execute(GetGraphQuery, {"id": id}, rath=rath).graph


async def asearch_graphs(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchGraphsQueryOptions]:
    """SearchGraphs

    List of all knowledge graphs

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGraphsQueryGraphs]"""
    return (
        await aexecute(
            SearchGraphsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_graphs(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchGraphsQueryOptions]:
    """SearchGraphs

    List of all knowledge graphs

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGraphsQueryGraphs]"""
    return execute(
        SearchGraphsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_protocol_step(id: ID, rath: Optional[KraphRath] = None) -> ProtocolStep:
    """GetProtocolStep


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ProtocolStep"""
    return (await aexecute(GetProtocolStepQuery, {"id": id}, rath=rath)).protocol_step


def get_protocol_step(id: ID, rath: Optional[KraphRath] = None) -> ProtocolStep:
    """GetProtocolStep


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ProtocolStep"""
    return execute(GetProtocolStepQuery, {"id": id}, rath=rath).protocol_step


async def asearch_protocol_steps(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchProtocolStepsQueryOptions]:
    """SearchProtocolSteps

    List of all protocol steps

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchProtocolStepsQueryProtocolsteps]"""
    return (
        await aexecute(
            SearchProtocolStepsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_protocol_steps(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchProtocolStepsQueryOptions]:
    """SearchProtocolSteps

    List of all protocol steps

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchProtocolStepsQueryProtocolsteps]"""
    return execute(
        SearchProtocolStepsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_entity_relation(
    id: ID, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """GetEntityRelation


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return (
        await aexecute(GetEntityRelationQuery, {"id": id}, rath=rath)
    ).entity_relation


def get_entity_relation(id: ID, rath: Optional[KraphRath] = None) -> EntityRelation:
    """GetEntityRelation


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return execute(GetEntityRelationQuery, {"id": id}, rath=rath).entity_relation


async def asearch_entity_relations(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchEntityRelationsQueryOptions]:
    """SearchEntityRelations

    List of all relationships between entities

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntityRelationsQueryEntityrelations]"""
    return (
        await aexecute(
            SearchEntityRelationsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_entity_relations(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchEntityRelationsQueryOptions]:
    """SearchEntityRelations

    List of all relationships between entities

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntityRelationsQueryEntityrelations]"""
    return execute(
        SearchEntityRelationsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_reagent(id: ID, rath: Optional[KraphRath] = None) -> Reagent:
    """GetReagent


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Reagent"""
    return (await aexecute(GetReagentQuery, {"id": id}, rath=rath)).reagent


def get_reagent(id: ID, rath: Optional[KraphRath] = None) -> Reagent:
    """GetReagent


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Reagent"""
    return execute(GetReagentQuery, {"id": id}, rath=rath).reagent


async def asearch_reagents(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchReagentsQueryOptions]:
    """SearchReagents

    List of all reagents used in protocols

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchReagentsQueryReagents]"""
    return (
        await aexecute(
            SearchReagentsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_reagents(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchReagentsQueryOptions]:
    """SearchReagents

    List of all reagents used in protocols

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchReagentsQueryReagents]"""
    return execute(
        SearchReagentsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_entity(id: ID, rath: Optional[KraphRath] = None) -> Entity:
    """GetEntity


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return (await aexecute(GetEntityQuery, {"id": id}, rath=rath)).entity


def get_entity(id: ID, rath: Optional[KraphRath] = None) -> Entity:
    """GetEntity


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return execute(GetEntityQuery, {"id": id}, rath=rath).entity


async def asearch_entities(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchEntitiesQueryOptions]:
    """SearchEntities

    List of all entities in the system

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntitiesQueryEntities]"""
    return (
        await aexecute(
            SearchEntitiesQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_entities(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchEntitiesQueryOptions]:
    """SearchEntities

    List of all entities in the system

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntitiesQueryEntities]"""
    return execute(
        SearchEntitiesQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aentities(
    filters: Optional[EntityFilter] = None,
    pagination: Optional[GraphPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[Entity]:
    """Entities

    List of all entities in the system

    Arguments:
        filters (Optional[EntityFilter], optional): No description.
        pagination (Optional[GraphPaginationInput], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[Entity]"""
    return (
        await aexecute(
            EntitiesQuery, {"filters": filters, "pagination": pagination}, rath=rath
        )
    ).entities


def entities(
    filters: Optional[EntityFilter] = None,
    pagination: Optional[GraphPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[Entity]:
    """Entities

    List of all entities in the system

    Arguments:
        filters (Optional[EntityFilter], optional): No description.
        pagination (Optional[GraphPaginationInput], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[Entity]"""
    return execute(
        EntitiesQuery, {"filters": filters, "pagination": pagination}, rath=rath
    ).entities


async def alist_paired_entities(
    graph: ID,
    relation_filter: Optional[EntityRelationFilter] = None,
    left_filter: Optional[EntityFilter] = None,
    right_filter: Optional[EntityFilter] = None,
    pagination: Optional[GraphPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[ListPairedEntitiesQueryPairedentities]:
    """ListPairedEntities

    Retrieves paired entities

    Arguments:
        graph (ID): The graph to query the paired entities from
        relation_filter (Optional[EntityRelationFilter], optional): The filter to apply to the relation.
        left_filter (Optional[EntityFilter], optional): The filter to apply to the left side of the relation.
        right_filter (Optional[EntityFilter], optional): The filter to apply to the right side of the relation.
        pagination (Optional[GraphPaginationInput], optional): The pagination to apply to the query.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[ListPairedEntitiesQueryPairedentities]"""
    return (
        await aexecute(
            ListPairedEntitiesQuery,
            {
                "graph": graph,
                "relationFilter": relation_filter,
                "leftFilter": left_filter,
                "rightFilter": right_filter,
                "pagination": pagination,
            },
            rath=rath,
        )
    ).paired_entities


def list_paired_entities(
    graph: ID,
    relation_filter: Optional[EntityRelationFilter] = None,
    left_filter: Optional[EntityFilter] = None,
    right_filter: Optional[EntityFilter] = None,
    pagination: Optional[GraphPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[ListPairedEntitiesQueryPairedentities]:
    """ListPairedEntities

    Retrieves paired entities

    Arguments:
        graph (ID): The graph to query the paired entities from
        relation_filter (Optional[EntityRelationFilter], optional): The filter to apply to the relation.
        left_filter (Optional[EntityFilter], optional): The filter to apply to the left side of the relation.
        right_filter (Optional[EntityFilter], optional): The filter to apply to the right side of the relation.
        pagination (Optional[GraphPaginationInput], optional): The pagination to apply to the query.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[ListPairedEntitiesQueryPairedentities]"""
    return execute(
        ListPairedEntitiesQuery,
        {
            "graph": graph,
            "relationFilter": relation_filter,
            "leftFilter": left_filter,
            "rightFilter": right_filter,
            "pagination": pagination,
        },
        rath=rath,
    ).paired_entities


async def aget_ontology(id: ID, rath: Optional[KraphRath] = None) -> Ontology:
    """GetOntology


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Ontology"""
    return (await aexecute(GetOntologyQuery, {"id": id}, rath=rath)).ontology


def get_ontology(id: ID, rath: Optional[KraphRath] = None) -> Ontology:
    """GetOntology


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Ontology"""
    return execute(GetOntologyQuery, {"id": id}, rath=rath).ontology


async def asearch_ontologies(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchOntologiesQueryOptions]:
    """SearchOntologies

    List of all ontologies

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchOntologiesQueryOntologies]"""
    return (
        await aexecute(
            SearchOntologiesQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_ontologies(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchOntologiesQueryOptions]:
    """SearchOntologies

    List of all ontologies

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchOntologiesQueryOntologies]"""
    return execute(
        SearchOntologiesQuery, {"search": search, "values": values}, rath=rath
    ).options


LinkedExpressionFilter.model_rebuild()
ProtocolStepInput.model_rebuild()
StructureRelationInput.model_rebuild()
