# PyRunbookManager
Easily install PIP dependencies in your azure runbook at runtime.
# Setup
- Download the .whl build from the [PyPI project page](https://pypi.org/project/PyRunbookManager/)
- Add it as a module in your runtime environment
# Usage
To install additional modules, you must first import PyRunbookManager.
```python
from PyRunbookManager import modulemanager
```
## Installing a module
```python
from PyRunbookManager import modulemanager
modulemanager.install("requests")
import requests
```
## installing a list of modules
```python
from PyRunbookManager import modulemanager
dependencies = ['requests','os']
for module in dependencies:
    modulemanager.install(module)

import os
import requests
```
## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or inquiries, please open an issue.

## Disclaimer
I am not responsible for any damage and/or misuse as a result of using this lib.
