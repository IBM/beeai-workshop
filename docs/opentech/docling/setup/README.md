# Docling notebook setup

Launch Jupyter with `doclingkernel` which has the dependencies from our `pyproject.toml` venv.

```shell
uv run --directory docling ipython kernel install --user --env VIRTUAL_ENV .venv --name=doclingkernel
uv run --directory docling jupyter lab
```

In Jupyter Lab:

* Double-click the notebooks folder
* Double-click the Conversion.ipynb
* Use the play button to walk through the notebook
