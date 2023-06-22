from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field


class PublicationBacked(BaseModel):
    publications: List[Dict[str, str]] = Field([], description="List of related publications and associated metadata.")


class Phenotype(PublicationBacked):
    phenotype_id: str = Field(
        ..., description="The ontology identifier of the phenotype.", example="HP:0002721"
    )
    label: str = Field(
        ..., description="The human-readable label of the phenotype.", example="Immunodeficiency"
    )


class PhenotypeAssociation(PublicationBacked):
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
    phenotype_url_template: str = Field(..., description="URL template for constructing links to the Monarch Initiative website.", example="https://monarchinitiative.org/phenotype/{phenotype_id}")


class Disease(PublicationBacked):
    disease_id: str = Field(
        ..., description="The ontology identifier of the disease.", example="MONDO:0009061"
    )
    label: str = Field(
        ..., description="The human-readable label of the disease.", example="cystic fibrosis"
    )


class DiseaseAssociation(PublicationBacked):
    disease: Disease = Field(..., description="The Disease object.")
    type: Optional[str] = Field(
        None, description="The type of the association (causal or correlated)."
    )


class DiseaseAssociations(BaseModel):
    associations: List[DiseaseAssociation] = Field(
        ..., description="The list of DiseaseAssociation objects."
    )
    total: int = Field(..., description="The total number of disease associations available.")
    disease_url_template: str = Field(..., description="URL template for constructing links to the Monarch Initiative website.", example="https://monarchinitiative.org/disease/{disease_id}")


class Gene(PublicationBacked):
    gene_id: str = Field(..., description="The ontology identifier of the gene.", example="HGNC:1884")
    label: str = Field(..., description="The human-readable label of the gene.", example="CFTR")


class GeneAssociation(PublicationBacked):
    gene: Gene


class GeneAssociations(BaseModel):
    associations: List[GeneAssociation] = Field(
        ..., description="The list of GeneAssociation objects."
    )
    total: int = Field(..., description="The total number of gene associations available.")
    gene_url_template: str = Field(..., description="URL template for constructing links to the Monarch Initiative website.", example="https://monarchinitiative.org/gene/{gene_id}")





class AssociationCount(BaseModel):
    label: str = Field(..., description="The type of the associations (e.g. Disease or Gene)", example="Causal")
    count: int = Field(..., description="The number of associations of that type.")


class Entity(BaseModel):
    id: str = Field(..., description="The ontology identifier of the entity.", example="MONDO:0009061")
    category: List[str] = Field(..., description="The categories of the entity.", example=["biolink:Disease"])
    name: Optional[str] = Field(None, description="The human-readable label of the entity.", example="cystic fibrosis")
    description: Optional[str] = Field(None, description="The description of the entity.")
    symbol: Optional[str] = Field(None, description="The symbol of the entity, usually a short name like FBN1.")
    synonym: List[str] = Field(..., description="The synonyms of the entity.")
    association_counts: List[AssociationCount] = Field(..., description="Counts of associations between this entity and other entities of different types.")
