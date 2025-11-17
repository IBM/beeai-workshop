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
cd beeai-workshop/opentech
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

## Lab

The path of the notebooks directory is relative to the `opentech/docling` folder from the git clone in the [prework](../prework/README.md).

1. Run the following commands to create `doclingkernel` which has the dependencies from our `pyproject.toml` venv and launch Jupyter Lab.

    ```shell
    uv run --directory docling ipython kernel install --user --env VIRTUAL_ENV .venv --name=doclingkernel
    uv run --directory docling jupyter lab
    ```

1. In Jupyter Lab in your browser, walk through the notebook:

    1. Jupyter Lab will open in your browser
    1. Navigate to the `notebooks` folder
    1. Open `Conversion.ipynb`
    1. Use the play button to walk through the notebook
    1. Be sure to read the text, the code, and the output
