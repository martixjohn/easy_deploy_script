## Introduction

Scripts providing an convenient way to deploy or install the binary etc. 

This Script can be used to **COPY** dlls, binaries, docs, etc.

It will **searches the specified files recursively in directories and copies them to the destination**


## Prerequisites

Python 3 MUST be installed

## How to use


```shell
python deploy.py [configuration_file] [out_dir]
```
- configuration_file: The file path including configurations 

- out_dir \[optional\]: the destination directory

#### Configuration File

Configuration-File Must be type of JSON

Here is an example:

```json
{
  "targets": [
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

**The Details For the Keys in JSON:**

- targets: what you want to copy, which are the names of the files

- search_dirs: where to search the targets

- out_dir \[optional\]: the destination directory. When `out_dir` arg is given, this will be ignored