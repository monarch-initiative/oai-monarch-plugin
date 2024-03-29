# The following code provides a thin wrapper around the Monarch API
# to provide a simple API for the OpenAI plugin to use. It uses FastAPI
# and is run on port 3434 by default.

from os.path import abspath, dirname
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import os

# local imports
from .logger_config import configure_logger
from .middlewares import LoggingMiddleware

from .routers import (
    disease_to_gene,
    phenotype_profile_search,
    disease_to_phenotype,
    gene_to_disease,
    gene_to_phenotype,
    phenotype_to_disease,
    phenotype_to_gene,
    search,
    entity
)

# setup base app
app = FastAPI()

# setup logging
configure_logger()
app.middleware("http")(LoggingMiddleware())

# setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# dynamically generate ai-plugin.json with dev/prod hostnames
@app.get("/.well-known/ai-plugin.json")
async def get_ai_plugin():
    # Load the json file
    with open(f"{dirname(abspath(__file__))}/.well-known/ai-plugin.json", "r") as f:
        data = json.load(f)
    
    # Modify fields based on environment variables
    if os.getenv("OAI_PLUGIN_HOST_PORT"):
        data['api']['url'] = f"{os.getenv('OAI_PLUGIN_HOST_PORT')}/openapi.json"
        data['logo_url'] = f"{os.getenv('OAI_PLUGIN_HOST_PORT')}/static/logo.png"

    return data

app.mount("/static", StaticFiles(directory=dirname(abspath(__file__)) + "/static"), name="static")

# setup routers
app.include_router(search.router)
app.include_router(phenotype_profile_search.router)
app.include_router(entity.router)
app.include_router(disease_to_gene.router)
app.include_router(disease_to_phenotype.router)
app.include_router(gene_to_disease.router)
app.include_router(gene_to_phenotype.router)
app.include_router(phenotype_to_disease.router)
app.include_router(phenotype_to_gene.router)
