# yuno-py-utils

Utils for python

## Getting Started

```shell
pip install yunopyutils
```

or using PDM

```python
pdm add yunopyutils
```

## Modules

### Logs

```python
from yunopyutils import build_logger

logger = build_logger(__file__)

logger.info("Hello World !")

# Expected result
## {"timestamp": "2023-06-16T15:25:02.469Z", "level": "INFO", "filename": "log.py", "module": "log", "line": 5, "message": "Hello World !"}
```
