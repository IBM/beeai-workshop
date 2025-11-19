---
title: Docling Workshop Lab 1
description: Document Conversion with Docling
logo: images/DoclingDuck.png
---

# Document Conversion with Docling

The primary purpose of Docling is document conversion. Docling enables us to convert documents various format into formats that are more useful in AI applications, while preserving document structure.

This lab walks through the different document conversion options Docling offers, as well as some enrichment features. We will also explore the converted documents to examine how Docling stores metadata to preserve document structure.

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

    1. Jupyter Lab will open in your browser
    1. Navigate to the `notebooks` folder
    1. Open `Conversion.ipynb`
    1. Use the play button to walk through the notebook
    1. Be sure to read the text, the code, and the output
    1. Exit your browser tab
    1. Exit your Jupyter Lab server by entering CTRL-C, CTRL-C in your the terminal where it is running
