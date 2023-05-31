from fastapi import APIRouter, Query
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Phenotype(BaseModel):
    id: str = Field(..., description="The ontology identifier of the phenotype.", example="HP:0002721")
    label: str = Field(..., description="The human-readable label of the phenotype.", example="Immunodeficiency")

class PhenotypeAssociation(BaseModel):
    id: str = Field(..., description="The ontology identifier of the association.")
    frequency_qualifier: Optional[str] = Field(None, description="The frequency qualifier of the association.")
    onset_qualifier: Optional[str] = Field(None, description="The onset qualifier of the association.")
    phenotype: Phenotype

class PhenotypeAssociations(BaseModel):
    associations: List[PhenotypeAssociation] = Field(..., description="The list of PhenotypeAssociation objects.")
    total: int = Field(..., description="The total number of phenotype associations available.")




class Disease(BaseModel):
    id: str = Field(..., description="The ontology identifier of the disease.", example="MONDO:0009061")
    label: str = Field(..., description="The human-readable label of the disease.", example="cystic fibrosis")

class DiseaseAssociation(BaseModel):
    id: str = Field(..., description="The ontology identifier of the association.")
    disease: Disease

class DiseaseAssociations(BaseModel):
    associations: List[DiseaseAssociation] = Field(..., description="The list of DiseaseAssociation objects.")
    total: int = Field(..., description="The total number of disease associations available.")




class Gene(BaseModel):
    id: str = Field(..., description="The ontology identifier of the gene.", example="HGNC:1884")
    label: str = Field(..., description="The human-readable label of the gene.", example="CFTR")

class GeneAssociation(BaseModel):
    id: str = Field(..., description="The ontology identifier of the association.")
    gene: Gene

class GeneAssociations(BaseModel):
    associations: List[GeneAssociation] = Field(..., description="The list of GeneAssociation objects.")
    total: int = Field(..., description="The total number of gene associations available.")