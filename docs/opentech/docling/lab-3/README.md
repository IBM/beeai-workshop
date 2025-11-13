---
title: Docling Workshop Lab 3
description: Multimodal RAG with Docling
logo: images/DoclingDuck.png
---

# Multimodal RAG with Docling

[Retrieval Augmented Generation (RAG)](https://research.ibm.com/blog/retrieval-augmented-generation-RAG) is an architectural pattern that can be used to augment the performance of language models by recalling factual information from a knowledge base, and adding that information to the model query.

In this lab we will combine the skills we learned in the two previous labs to build a Docling-enhanced RAG system.

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
    1. Open `RAG.ipynb`
    1. Use the play button to walk through the notebook
    1. Be sure to read the text, the code, and the output
