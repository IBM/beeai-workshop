---
title: Prework
description: Demo Prework Instructions
logo: images/BeeAI-Logo-White.png
---

# BeeAI Platform Demo: Prework Instructions

Welcome to the Introduction to BeeAI Platform demo.  
Please complete the following setup steps **before** the demo.

---

## Python Environment Manager

### `uv` (Recommended)

We recommend using [`uv`](https://github.com/astral-sh/uv) as your Python package and environment manager.

- If you’re unfamiliar with `uv`, refer to the [uv installation guide](https://github.com/astral-sh/uv#installation)
- `uv` is a fast and modern alternative to pip and virtualenv, fully compatible with both

---

## Local Model

### Install Ollama

!!! note
    To run the Granite model locally, we recommend having at least **16GB of RAM** for optimal performance.

To run models locally on your machine:

1. Download and install Ollama: [https://ollama.com/download](https://ollama.com/download)
2. Run or pull the Granite model:

   ```bash
   ollama pull granite4:tiny-h
   ```

   or

   ```bash
   ollama run granite4:tiny-h
   ```

### Granite model links

- Ollama models: [Granite 4](https://ollama.com/library/granite4)
- Ollama models: [Granite 3.3](https://ollama.com/library/granite3.3)
- Granite docs: [Granite](https://www.ibm.com/granite/docs/models/granite)

---

## You're Ready

Once you've completed these steps, you're ready to setup the project.