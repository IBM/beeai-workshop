---
title: Prework
description: Workshop prework instructions
logo: images/BeeAI-Logo-White.png
---

# Prework

Please complete the following setup steps **before** the workshop.

---

## Local Models

### Install Ollama

!!! note
    To run the Granite model locally, we recommend having at least **16GB of RAM** for optimal performance.

To run models locally on your machine:

1. Download and install Ollama: [https://ollama.com/download](https://ollama.com/download)

2. Pull the models

    Please pull the models before the workshop!

    ```shell
    ollama pull ibm/granite4:micro
    ollama pull ibm/granite-embedding:30m
    ollama pull ibm/granite-docling
    ```

3. Quick test

    Test by chatting with a model (e.g., ask what model it is):

    ```shell
    ollama run granite4:micro "what model are you and who created you?"
    ```

    !!! note
        Don't be surprised by hallucination and different answers each time you run this.

---

## Python Environment Manager

### Install `uv`

We will be using [`uv`](https://github.com/astral-sh/uv) as your Python package and environment manager. If you’re unfamiliar with `uv`, refer to the [uv installation guide](https://github.com/astral-sh/uv#installation).

- `uv` is a fast and modern alternative to pip and virtualenv, fully compatible with both
- `uv` manages versioned installations of Python

For most people, the install guide provides a one-line install command:

#### On macOS/Linux

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### On Windows

```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Get the workshop code

**Option A: Clone with Git (recommended):**

```bash
git clone https://github.com/IBM/beeai-workshop.git
```

**Option B: Download ZIP:**

If you're not comfortable with Git, [download the ZIP](https://github.com/IBM/beeai-workshop/archive/refs/heads/main.zip) file and extract it to your desired location.

---

## Install project Python dependencies

Preinstall all the packages used in the demo, installed in the correct virtual environment using `uv`.

1. Navigate to the specific demo folder for this workshop:

    ```bash
    cd beeai-workshop/opentech
    ```

2. Install all required python dependencies for the 4 sub-projects:

    ```bash
    uv sync --directory docling
    uv sync --directory mellea
    uv sync --directory beeaiframework
    uv sync --directory agentstack
    ```

---

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

Once the downloads, install, and start are complete, you will have a fancy Open WebUI "get started" page at localhost:8080.  You can now kill the server with control-C back in the terminal. We'll do the setup during the workshop.

---

## Install Agent Stack

Ideally, everyone will get hands-on experience wrapping all the pieces together with Agent Stack. If you cannot run Agent Stack on your laptop, come to the workshop anyway!  We will demonstrate.

- Agent Stack quickstart: [https://agentstack.beeai.dev/introduction/quickstart](https://agentstack.beeai.dev/introduction/quickstart)
