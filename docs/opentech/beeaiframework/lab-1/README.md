---
title: Lab 1
description: Build an agent with BeeAI Framework
logo: images/BeeAI-Logo-White.png
---

# Build an agent with BeeAI Framework

## Prerequisites

This lab is a [Jupyter notebook](https://jupyter.org/). Please follow the instructions in [prework](../../prework/README.md) before you run the lab.

## Lab

1. Run the following commands to create `beekernel` which has the dependencies from our `pyproject.toml` venv and launch Jupyter Lab.

    ```shell
    uv run --directory beeai-framework ipython kernel install --user --env VIRTUAL_ENV .venv --name=beekernel
    uv run --directory beeai-framework jupyter lab
    ```

1. In Jupyter Lab in your browser, walk through the notebook:

    1. Jupyter Lab will open in your browser
    1. Navigate to the `notebooks` folder
    1. Open `beeai.ipynb`
    1. Use the play button to walk through the notebook
    1. Be sure to read the text, the code, and the output

1. Exit the Jupyter Lab server by typing CTRL-C, CTRL-C (twice) in the terminal window where you started Jupyter Lab.
