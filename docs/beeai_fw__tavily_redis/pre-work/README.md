---
title: Pre-work
description: Workshop Pre-work Instructions
logo: images/BeeAI-Logo-White.png
---

# BeeAI Framework Workshop: Prework Instructions

Welcome to the BeeAI Framework Workshop, in partnership with **Tavily** and **Redis**.  
Please complete the following setup steps **before** the workshop.

---

## Development Environment

### Device Memory Requirement (Recommended)


### Visual Studio Code (Recommended)

You may use any IDE, but this workshop assumes you're using **Visual Studio Code (VS Code)**.

- [Download Visual Studio Code (VS Code)](https://code.visualstudio.com/)
- Install the VS Code **Python and Jupyter extensions** from the Extensions Marketplace:
    1. Open the Extensions view in VS Code (`Ctrl+Shift+X` or `Cmd+Shift+X`)
    2. Search for “Python” by Microsoft and install it
    3. Search for "Jupyter" by Microsoft and install it

---

## Python Environment Manager

### `uv` (Recommended)

We recommend using [`uv`](https://github.com/astral-sh/uv) as your Python package and environment manager.

- If you’re unfamiliar with `uv`, refer to the [uv installation guide](https://github.com/astral-sh/uv#installation)
- `uv` is a fast and modern alternative to pip and virtualenv, fully compatible with both

---

## API Keys

### Tavily (Required)

- Go to [Tavily](https://app.tavily.com/home) and sign up for a free API key.

### OpenAI (Optional)

- Only needed if you do **not** plan to run a model locally with Ollama.
- [Get an OpenAI API Key](https://platform.openai.com/account/api-keys)

---

## Local Model (Optional if using OpenAI)

### Install Ollama

!!! note
    To run the Granite model locally, we recommend having at least **16GB of RAM** for optimal performance.

To run models locally on your machine:

1. Download and install Ollama: [https://ollama.com/download](https://ollama.com/download)
2. Run or pull the Granite model:

   ```bash
   ollama run granite3.3:8b
   ```

   or

   ```bash
   ollama pull granite3.3:8b
   ```

> Model link: [Granite 3.3:8b](https://ollama.com/library/granite3.3:8b)

---

## Redis Stack

We'll be using Redis Stack for local vector storage.

### Install Redis Stack

- Follow the [official installation instructions](https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-stack/)


---

## You're Ready

Once you've completed these steps, you're ready for the workshop.
