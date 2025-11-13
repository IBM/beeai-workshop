---
title: Docling Workshop Lab 2
description: Chunking and Vectorization with Docling
logo: images/DoclingDuck.png
---

# Chunking with Docling

[Chunking](https://www.ibm.com/architectures/papers/rag-cookbook/chunking) is the process of splitting large texts into smaller, manageable segments before feeding them into a model. This is an important step because models have a maximum context length, and chunking ensures that relevant information fits within this limit while preserving coherence, improving retrieval accuracy, and avoiding loss of important content during processing.

In this lab we will explore the importance of chunking and the capabilities Docling has to create more valuable chunks.

## Prerequisites

This lab is a [Jupyter notebook](https://jupyter.org/). Please follow the instructions in [prework](../prework/README.md) to run the lab.

## Lab

The path of the notebooks directory is relative to the `opentech/docling` folder from the git clone in the [prework](../prework/README.md).

1. (SKIP IF STILL RUNNING FROM LAB 1) Run the following commands to create `doclingkernel` which has the dependencies from our `pyproject.toml` venv and launch Jupyter Lab.

    ```shell
    uv run --directory docling ipython kernel install --user --env VIRTUAL_ENV .venv --name=doclingkernel
    uv run --directory docling jupyter lab
    ```

1. In Jupyter Lab in your browser, walk through the notebook:

    1. Navigate to the `notebooks` folder
    1. Open `Chunking.ipynb`
    1. Use the play button to walk through the notebook
    1. Be sure to read the text, the code, and the output
