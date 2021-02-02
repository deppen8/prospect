Installation
============

## Requirements

`prospect` is developed for use with Python 3.8 and above. `prospect` itself should be compatible with Python 3.6 and above, but some packages `prospect` depends on cannot be guaranteed to support other versions of Python.

```{tip}
You can see which packages `prospect` formally depends on by examining the [`setup.py` file](https://github.com/deppen8/prospect/blob/master/setup.py).
```

### Installing with `conda`

`prospect` is available from the `conda-forge` channel

```bash
$ conda install prospect -c conda-forge
```

## Using `conda` environments

`prospect` depends heavily on the `geopandas` package for handling spatial data. The GeoPandas team [recommends using the `conda` environment manager](https://geopandas.org/install.html) to help avoid some potential installation headaches, so the same goes for `prospect`: your best installation experience will be using `conda`.

If you run into installation troubles, you might first revisit the [GeoPandas installation instructions](https://geopandas.org/install.html) to see if your issue is addressed there.

```{tip}
If you are not familiar with using `conda`, I recommend these resources from the always-excellent EarthLab team:

- [Use Conda Environments to Manage Python Dependencies: Everything That You Need to Know](https://www.earthdatascience.org/courses/intro-to-earth-data-science/python-code-fundamentals/use-python-packages/introduction-to-python-conda-environments/)
- [Install Packages in Python](https://www.earthdatascience.org/courses/intro-to-earth-data-science/python-code-fundamentals/use-python-packages/use-conda-environments-and-install-packages/)
```

### Installing with `pip`

While it is not the recommended install strategy, `prospect` is available from PyPI.

```bash
$ python3 -m pip install prospect
```
