# Build everything

```
python3 -m build
```

may need ;

```
pip install build
```

# check everything is okay :

```
twine check dist/*
```

may need :

```
pip install twine
```

# Upload

```
twine upload dist/*
```
