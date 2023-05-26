# oai-monarch-plugin

ChatGPT plugin and wrapper for Monarch  API.

## How to run

### Get access to the ChatGPT plugin developer program

Unfortunately you will need to be accepted to the OpenAI developer program

Join the waitlist [here](https://openai.com/waitlist/plugins)

It may be possible to grant permissions broadly across an organization? https://community.openai.com/t/developer-access-for-colleagues/157315

### Run server/dev server/tests

Output of `make help`:

```bash
make all -- installs requirements, exports requirements.txt, runs production server
make dev -- installs requirements, runs hot-restart dev server
make test -- runs tests
make start -- runs production server
make start-dev -- runs hot-restart dev server
make export-requirements -- exports requirements.txt
make help -- show this help
```

The dev server currently runs on 3434, production 8080.

Check it works:

- http://localhost:3434/.well-known/ai-plugin.json
- http://localhost:3434/docs

### Register

Go to https://chat.openai.com/

If you have plugin access, you'll see an option

Select the plugin model from the top drop down, then select “Plugins”, “Plugin Store”, and finally “Install an unverified plugin” or “Develop your own plugin”.

Enter `localhost:3434`

You should see the plugin activated

If you run into difficulties, see https://platform.openai.com/docs/plugins/introduction

# Acknowledgements

This [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html) project was developed from the [monarch-project-template](https://github.com/monarch-initiative/monarch-project-template) template and will be kept up-to-date using [cruft](https://cruft.github.io/cruft/). Makefile modified from [Sierra Moxon's](https://github.com/geneontology/go-fastapi/blob/main/Makefile).
