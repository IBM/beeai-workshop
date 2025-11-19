---
title: BeeAI Framework Lab
description: BeeAI Framework Lab
logo: images/BeeAI-Logo-White.png
---

# Build an agent with BeeAI Framework

## Prerequisites

This lab is a [Jupyter notebook](https://jupyter.org/). Please follow the instructions in [prework](../prework/README.md) for the prerequisites to run the lab.

## Lab

Launch Jupyter Lab by running the following commands from the `opentech` directory of your `beeai-workshop` cloned repo.

1. Create `beekernel` which will have the dependencies preinstalled in your virtual environment.

    ```shell
    uv run --directory docling ipython kernel install --user --env VIRTUAL_ENV .venv --name=beekernel
    ```

2. Use `uv` to run Jupyter Lab. The directory and allow_hidden gives us access to `.venv` modules.

    ```shell
    uv run --directory docling jupyter lab --ContentsManager.allow_hidden=True
    ```

3. In Jupyter Lab in your browser, walk through the notebook:

    1. Jupyter Lab will open in your browser
    1. Navigate to the `notebooks` folder
    1. Open `beeai.ipynb`
    1. Use the play button to walk through the notebook
    1. Be sure to read the text, the code, and the output
    1. Close your browser tab when done

4. Exit the Jupyter Lab server by typing CTRL-C, CTRL-C (twice) in the terminal window where you started Jupyter Lab.
