from dataclasses import dataclass
from typing import Set

from typing_extensions import Literal

from tdm.abstract.datamodel import AbstractDomainType, Identifiable


@dataclass(frozen=True)
class _AbstractConceptType(AbstractDomainType):
    metatype: str

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return {'metatype'}


@dataclass(frozen=True)
class AbstractConceptType(Identifiable, _AbstractConceptType):
    pass


@dataclass(frozen=True)
class ConceptType(AbstractConceptType):
    metatype: Literal['concept'] = 'concept'


@dataclass(frozen=True)
class DocumentType(AbstractConceptType):
    metatype: Literal['document'] = 'document'
