---
title: Docling Workshop Lab 1
description: Document Conversion with Docling
logo: images/DoclingDuck.png
---

# Document Conversion with Docling

The primary purpose of Docling is document conversion. Docling enables us to convert documents various format into formats that are more useful in AI applications, while preserving document structure.

This lab walks through the different document conversion options Docling offers, as well as some enrichment features. We will also explore the converted documents to examine how Docling stores metadata to preserve document structure.

## Prerequisites

This lab is a [Jupyter notebook](https://jupyter.org/). Please follow the instructions in [prework](../prework/README.md) to run the lab.

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
