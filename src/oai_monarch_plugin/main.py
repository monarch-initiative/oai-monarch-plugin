# The following code provides a thin wrapper around the Monarch API
# to provide a simple API for the OpenAI plugin to use. It uses FastAPI
# and is run on port 3434 by default.


from enum import Enum
from typing import Any, Dict, List, Optional

import httpx
from fastapi import FastAPI, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from os.path import abspath, dirname
from .routers import search, disease_to_gene, disease_to_phenotype, gene_to_phenotype, gene_to_disease

BASE_API_URL = "https://api-dev.monarchinitiative.org/v3/api"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Serve static files needed for OpenAI plugin
app.mount("/.well-known", StaticFiles(directory = dirname(abspath(__file__)) + "/.well-known"), name="well-known")
app.mount("/static", StaticFiles(directory = dirname(abspath(__file__)) + "/static"), name="static")

app.include_router(search.router)
app.include_router(gene_to_phenotype.router)
app.include_router(disease_to_gene.router)
app.include_router(disease_to_phenotype.router)
app.include_router(gene_to_disease.router)