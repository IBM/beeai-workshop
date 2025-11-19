---
title: Mellea Workshop Pre-Work
description: Install pre-requisites for the workshop
logo: images/ibm-blue-background.png
---

These are the required applications and general installation notes for this workshop.

## Required Software and Models

- [uv](#install-uv) - Provides Python, packages, and virtual environments.
- [Ollama](#install-ollama) - Allows you to locally host LLM models on your computer.
- [Models](#pull-models-with-ollama) - Pull models to run with Ollama.
- [Workshop Code](#get-the-workshop-code) - Git clone the workshop

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
ollama pull ibm/granite4:micro-h
```

## Chat with the model

For a quick test, you can use the ollama CLI to ask the model a question.

```shell
ollama run ibm/granite4:micro-h "what model am I chatting with and and who created you?"  
```

## Get the workshop code

**Option A: Clone with Git (recommended):**

```bash
git clone https://github.com/IBM/beeai-workshop.git
```

**Option B: Download ZIP:**

If you're not comfortable with Git, [download the ZIP](https://github.com/IBM/beeai-workshop/archive/refs/heads/main.zip) file and extract it to your desired location.

Then:

```bash
cd beeai-workshop/opentech
```
