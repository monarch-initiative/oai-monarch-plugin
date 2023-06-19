from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field


class Phenotype(BaseModel):
    phenotype_id: str = Field(
        ..., description="The ontology identifier of the phenotype.", example="HP:0002721"
    )
    label: str = Field(
        ..., description="The human-readable label of the phenotype.", example="Immunodeficiency"
    )


class PhenotypeAssociation(BaseModel):
    frequency_qualifier: Optional[str] = Field(
        None, description="The frequency qualifier of the association."
    )
    onset_qualifier: Optional[str] = Field(
        None, description="The onset qualifier of the association."
    )
    phenotype: Phenotype


class PhenotypeAssociations(BaseModel):
    associations: List[PhenotypeAssociation] = Field(
        ..., description="The list of PhenotypeAssociation objects."
    )
    total: int = Field(..., description="The total number of phenotype associations available.")
    phenotype_url_template: str = Field(..., description="URL template for constructing links to the Monarch Initiative website.")


class Disease(BaseModel):
    disease_id: str = Field(
        ..., description="The ontology identifier of the disease.", example="MONDO:0009061"
    )
    label: str = Field(
        ..., description="The human-readable label of the disease.", example="cystic fibrosis"
    )


class DiseaseAssociation(BaseModel):
    disease: Disease = Field(..., description="The Disease object.")
    type: Optional[str] = Field(
        None, description="The type of the association (causal or correlated)."
    )


class DiseaseAssociations(BaseModel):
    associations: List[DiseaseAssociation] = Field(
        ..., description="The list of DiseaseAssociation objects."
    )
    total: int = Field(..., description="The total number of disease associations available.")
    disease_url_template: str = Field(..., description="URL template for constructing links to the Monarch Initiative website.")


class Gene(BaseModel):
    gene_id: str = Field(..., description="The ontology identifier of the gene.", example="HGNC:1884")
    label: str = Field(..., description="The human-readable label of the gene.", example="CFTR")


class GeneAssociation(BaseModel):
    gene: Gene


class GeneAssociations(BaseModel):
    associations: List[GeneAssociation] = Field(
        ..., description="The list of GeneAssociation objects."
    )
    total: int = Field(..., description="The total number of gene associations available.")
    gene_url_template: str = Field(..., description="URL template for constructing links to the Monarch Initiative website.")





class AssociationCount(BaseModel):
    label: str = Field(..., description="The type of the associations (e.g. Disease or Gene)", example="Causal")
    count: int = Field(..., description="The number of associations of that type.")


class Entity(BaseModel):
    id: str = Field(..., description="The ontology identifier of the entity.", example="MONDO:0009061")
    category: str = Field(..., description="The category of the entity.", example="biolink:Disease")
    name: str = Field(..., description="The human-readable label of the entity.", example="cystic fibrosis")
    description: Optional[str] = Field(None, description="The description of the entity.")
    symbol: Optional[str] = None
    synonym: List = []
    association_counts: List[AssociationCount]
