---
title: Workshop Pre-Work
description: Install pre-requisites for the workshop
logo: images/ibm-blue-background.png
---

These are the required applications and general installation notes for this workshop.

## Required Software and Models

- [uv](#install-uv) - Provides Python, packages, and virtual environments.
- [Ollama](#install-ollama) - Allows you to locally host LLM models on your computer.
- [Models](#pull-models-with-ollama) - Pull models to run with Ollama.
- [Open WebUI](#install-open-webui) - A UI that works with Ollama models.

## Install `uv`

We will be using [`uv`](https://github.com/astral-sh/uv) as your Python package and environment manager. If you’re unfamiliar with `uv`, refer to the [uv installation guide](https://github.com/astral-sh/uv#installation). `uv` is a fast and modern alternative to pip and virtualenv, fully compatible with both.

### macOS/Linux

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Install Ollama

Most users can simply download from the Ollama [website](https://ollama.com/download).

## Pull models with Ollama

Please pull the models to be used in the workshop before arriving at the workshop!

```shell
ollama pull granite4:micro-h
```

## Chat with the model

For a quick test, you can use the ollama CLI to ask the model a question.

```shell
ollama run granite4:micro-h "what model am I chatting with and and who created you?"  
```

## Install Open WebUI

Once uv is installed, use `uvx` to run Open WebUI with Python 3.11 (recommend for Open WebUI).

### macOS/Linux

```shell
DATA_DIR=~/.open-webui uvx --python 3.11 open-webui@latest serve
```

### Windows

```shell
$env:DATA_DIR="C:\open-webui\data"; uvx --python 3.11 open-webui@latest serve
```

Once the downloads, install, and start are complete, you will have a fancy Open WebUI "get started" page at localhost:8080.  You can now kill the server with Control-C back in the terminal. We'll do the setup during the workshop.
