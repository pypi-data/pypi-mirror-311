# copytrav
## Copying Python Traversals
Modern Python packaging has support for data files to be included with the
package alongside source files. There are many times when you might want to
have copies of these files on disk, often when being used with external or
third-party programs, and this is the role copytrav fills. You may, of course,
use [`importlib.resources.as_file(traversable)`](https://docs.python.org/3/library/importlib.resources.html#importlib.resources.as_file),
but there are still other times when a context manager isn't good enough.

## Users
### Installation
`pip install copytrav`

### Usage
#### Copying a Directory
```
from copytrav import copy

copy("mymodule.data", "path/to_directory", "output_path")
```

#### Copying a File
```
from copytrav import copy

copy("mymodule.data", "path/to_file", "output_path")
```

#### Copy the Whole Module
```
from copytrav import copy

copy("mymodule.data", dst="output_path")
```

#### Copy the Whole Module into a TempDir
```
from copytrav import copy

tempdir = copy("mymodule.data")
```

## Building the Documentation
clone the repository

```
pip install -e .[dev]

cd docs && make html
```
