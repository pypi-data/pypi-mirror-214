# Al Bhed

Simple CLI and Library that translates Text into Al Bhed

Python:
```python
>>> from albhed import AlBhed
>>>
>>> albhed = AlBhed("Hello, World!")
>>> albhed.translate()
'Rammu, Funmt!'
>>>
>>> albhed = AlBhed("Rammu, Funmt!")
>>> albhed.revert()
'Hello, World!'
```

Shell:
```shell
$ albhed Hello, World!
Rammu, Funmt!

$ albhed -r Rammu, Funmt!
Hello, World!
```
