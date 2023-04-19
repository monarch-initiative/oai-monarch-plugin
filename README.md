# Monarch OpenAI Plugin (Alpha Test)

This repo contains a small shim API that wraps the Monarch API, providing just a search endpoint and a genes-for-disease endpoint for proof-of-concept. It is designed to be used as an OpenAI ChatGPT plugin, so the .well-known folder contains an `ai-plugin.json` and the plugin also calls the default `/openapi.json` provided by FastAPI. 

Currently the search and list-genes endpoint work ok when run from the `run_test_queries.sh` script, but the plugin is only working
with the search endpoint. It seems unable to properly call the other endpoint though, as a request doesn't even show up in the logs.

