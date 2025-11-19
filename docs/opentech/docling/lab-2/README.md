---
title: Docling Workshop Lab 2
description: Chunking and Vectorization with Docling
logo: images/DoclingDuck.png
---

# Chunking with Docling

[Chunking](https://www.ibm.com/architectures/papers/rag-cookbook/chunking) is the process of splitting large texts into smaller, manageable segments before feeding them into a model. This is an important step because models have a maximum context length, and chunking ensures that relevant information fits within this limit while preserving coherence, improving retrieval accuracy, and avoiding loss of important content during processing.

In this lab we will explore the importance of chunking and the capabilities Docling has to create more valuable chunks.

## Prerequisites

This lab is a [Jupyter notebook](https://jupyter.org/). Please follow the instructions in [prework](../prework/README.md) for the prerequisites to run the lab.

## Lab

Launch Jupyter Lab by running the following commands from the `opentech` directory of your `beeai-workshop` cloned repo.

1. Create `doclingkernel` which will have the dependencies preinstalled in our virtual environment.

    ```shell
    uv run --directory docling ipython kernel install --user --env VIRTUAL_ENV .venv --name=doclingkernel
    ```

2. Use `uv` to run Jupyter Lab. The directory and allow_hidden gives us access to `.venv` modules.

    ```shell
    uv run --directory docling jupyter lab --ContentsManager.allow_hidden=True
    ```

3. In Jupyter Lab in your browser, walk through the notebook:

    1. Navigate to the `notebooks` folder
    1. Open `Chunking.ipynb`
    1. Use the play button to walk through the notebook
    1. Be sure to read the text, the code, and the output
    1. Exit your browser tab
    1. Exit your Jupyter Lab server by entering CTRL-C, CTRL-C in your the terminal where it is running
