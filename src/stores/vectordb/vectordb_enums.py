from enum import Enum


class VectordbEnum(Enum):
    QDRANT = "QDRANT"


class DistanceMethodEnum(Enum):
    COSINE = "cosine"
    DOT = "dot"
