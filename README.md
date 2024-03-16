# treediff

An utility for comparing files in 2 folders

## Usage:
```
usage: $ treediff [options...] <left> <right>
  Note: <left> and <right> can be a pair of files or a pair of directories

Examples:
To compare files in 2 directories dir_a and dir_b
  $ treediff dir_a dir_b

To compare files in 2 directories dir_a and dir_b, included subfolders
  $ treediff dir_a dir_b --recursive

To compare specific files (*.txt, *.psd) in 2 directories dir_a and dir_b
  $ treediff --filter .txt .psd dir_a dir_b

Exit code:
 0  : directories or files are the same
 1  : directories or files are different
 255: an error/exception occured

Utility for comparing directory/file

positional arguments:
  left                  specify left dir/file
  right                 specify right dir/file

options:
  -h, --help            show this help message and exit
  -r, --recursive       search file recursively
  -q, --quiet           be quiet
  -f FILTER [FILTER ...], --filter FILTER [FILTER ...]
                        file filters separated by space. Ex: -f .psd .txt ...
```

## How to use

To compare 2 directories:
```
$ treediff dir_a dir_b
dir_a/           !=  dir_b/
    file_1.txt   ==      file_1.txt
    file_2.txt   ==      file_2.txt
    file_3.txt   !=      file_3.txt
    file_4.txt   ==      file_4.txt
    file_5.txt   !=      ...
    ...          !=      file_6.txt
    log_1.log    ==      log_1.log
    log_2.log    ==      log_2.log
    log_5.log    ==      log_5.log
    log_6.log    !=      ...
    sub_dir/     ==      sub_dir/

```

To compare 2 directories included their sub directories: use `-r/--recursive` option.
```
$ treediff dir_a dir_b -r
dir_a/               !=  dir_b/
    file_1.txt       ==      file_1.txt
    file_2.txt       ==      file_2.txt
    file_3.txt       !=      file_3.txt
    file_4.txt       ==      file_4.txt
    file_5.txt       !=      ...       
    ...              !=      file_6.txt
    log_1.log        ==      log_1.log
    log_2.log        ==      log_2.log
    log_5.log        ==      log_5.log
    log_6.log        !=      ...
    sub_dir/         !=      sub_dir/
        file1.log    ==          file1.log
        file2.log    !=          file2.log
        file3.log    ==          file3.log
        ...          !=          file4.log
        file5.log    !=          ...

```

To compare only *.txt files in 2 directories, use `-f/--filter option`. 
Note: You can specify multiple file types also, for example: `-f .txt .log`

```
$ treediff dir_a dir_b -r -f .txt 
dir_a/           !=  dir_b/
    file_1.txt   ==      file_1.txt
    file_2.txt   ==      file_2.txt
    file_3.txt   !=      file_3.txt
    file_4.txt   ==      file_4.txt
    file_5.txt   !=      ...
    ...          !=      file_6.txt
    sub_dir/     ==      sub_dir/
```


Or you can also just compare 2 files

```
$ treediff dir_a\file_1.txt dir_b\file_1.txt

INFO: 2 files are identical at binary level
```

## How to build and install

To build this project, run the following commands

```

$ git clone <this_repo_url>   <-- clone this project
$ cd treediff                 <-- move to project directory
$ pip install build           <-- install 'build' package, do this only once if not installed
$ python -m build             <-- build this project

```


After build this project, use the following command to install

```
$ pip install dist\treediff-<version>-py3-none-any.whl --force-reinstall
```


