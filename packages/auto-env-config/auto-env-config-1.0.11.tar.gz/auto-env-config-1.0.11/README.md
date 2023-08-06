```python
import os
import sys
os.system(f'{sys.executable} -m pip install auto-env-config')
```
### Use requirements.txt
```python
import aec
aec.install('requirements.txt')
```
### Use config
```json
{
  "pip_index": "https://pypi.org/simple",
  "packages": [
    {
      "package_name": "numpy",
      "version": "1.22.0"
    }
  ]
}
```
```python
import aec
aec.install('install.config.json')
```
