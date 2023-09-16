## Introduction

Scripts providing an convenient way to deploy or install the binary etc. 

## Prerequisites
Python 3 must be installed

#### deploy.py

**search the specified files recursively in directories and copy them to the destination**


```shell
python deploy.py [configuration_file]
```
- configuration_file: The file path including configurations 

#### configuration_file

Here is an example:

```json
{
  "target": [
    "a.dll",
    "b.dll",
    "c.exe"
  ],
  "search_dirs": [
    "./bin/a",
    "./bin/b"
  ],
  "out_dir": "./install"
}
```


