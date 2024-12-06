# parsync

Parsync lets you recursively copy missing files to a directory.

This is equivalent to `cp -r --ignore-existing SRC DST` but using concurrent copies to accelerate the process.

## Example

Copy the content of the current directory:

`parsync * /dest`

Copy with 2 threads:

`parsync -p 2 src dest`

Copy only jpeg files and skip a specific directory, note the usage of [python regex syntax]([text](https://docs.python.org/3/library/re.html#regular-expression-syntax)):

`parsync --filter='\.jpg$' --exclude='/somedir/' src dest`

## Usage

```
usage: parsync [-h] [--procs PROCS] [--filter [FILTER ...]] [--exclude [EXCLUDE ...]] [--version] SRC [SRC ...] DST

Recursively copy missing files to a directory.

This is equivalent to: cp -r --ignore-existing SRC DST

Note: matching patterns use python regex syntax.

positional arguments:
  SRC                   source files and directories
  DST                   destination directory

options:
  -h, --help            show this help message and exit
  --procs PROCS, -p PROCS
                        maximum number of concurrent copies
  --filter [FILTER ...], -f [FILTER ...]
                        pattern to filter source files
  --exclude [EXCLUDE ...], -e [EXCLUDE ...]
                        pattern to exclude source files
  --version, -v         show program's version number and exit
  ```