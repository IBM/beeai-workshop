---
title: BeeAI Framework Workshop Prework
description: Preparation for the lab
logo: images/BeeAI-Logo-White.png
---

These are the required applications and general installation notes for this lab.

## Required Software and Models

- [Ollama](#install-ollama) - Allows you to locally host LLM models on your computer.
- [Models](#pull-models-with-ollama) - Pull models to run with Ollama.
- [uv](#install-uv) - Provides Python, packages, and virtual environments.

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

## Install project Python dependencies

Preinstall all the packages used in the demo, installed in the correct virtual environment using `uv`.

1. Navigate to the specific demo folder for this workshop:

    ```bash
    cd beeai-workshop/opentech
    ```

2. Install all required python dependencies for the project:

    ```bash
    uv sync --directory beeaiframework
    ```
