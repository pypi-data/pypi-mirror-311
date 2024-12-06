Batteries to complement the standard library (Python)

# Build and Install

Install all packages that are specified in `requirements-to-build.txt`. They can be `pip`-installed all at once with the following command.

```
python -m pip install -r requirements-to-build.txt
```

To build / pack up, run the following command at the top directory.

```
python -m build
```

A `.whl` is generated at directory `dist` which can then be `pip`-installed like so.

```
python -m pip install dist\jl95terceira_batteries-...whl
```
