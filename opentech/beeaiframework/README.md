# Intro to BeeAI Framework

If you didn't already do the prework for the entire workshop,
the steps specific to this hands-on lab are as follows:

## Python Environment Manager

### Install `uv`

We will be using [`uv`](https://github.com/astral-sh/uv) as your Python package and environment manager.

- If you’re unfamiliar with `uv`, refer to the [uv installation guide](https://github.com/astral-sh/uv#installation)
- `uv` is a fast and modern alternative to pip and virtualenv, fully compatible with both

## Navigate to the workshop folder

Navigate to the workshop folder:

```bash
cd beeai-workshop/beeai_docling_mellea
```

## Install Project Python Dependencies

**Install all required python dependencies for the lab:**

```bash
uv sync --directory beeai-framework
```

This ensures you have the correct versions of all packages used in the lab, installed in the correct environment.

> Note: In this case we are using UV to set up Python, jupyter, and pre-install the modules that will be used in the notebook.

## Run the notebook

Start the notebook by running the following `uv` command in a terminal.  Jupyter will load the notebook in your browser.  Follow the instructions in the notebook and run each cell.

```bash
uv --directory beeai-framework run --with jupyter jupyter notebook notebooks/beeai_framework_workshop_conference_agent.ipynb
```
