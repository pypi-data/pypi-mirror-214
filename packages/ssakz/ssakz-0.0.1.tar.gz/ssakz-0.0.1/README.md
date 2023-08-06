# Python API client for ssa.fai.kz

## Install
```bash
pip install ssakz
```

## Usage
```python
from ssakz import Client
client = Client("<your API key>")
```
The API key is available upon registering at ssa.fai.kz

```python
# Query near-miss events, starting from 2023-06-19,
# where the minimal predicted distance between objects is less than 30 km
nme = client.get_nme(rhigh=30, since='2023-06-19')
```
