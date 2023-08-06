# Fudan Utilities

- [Fudan Utilities](#fudan-utilities)
  - [Installation](#installation)
    - [pipx](#pipx)
    - [pip](#pip)
  - [Supplying your credentials](#supplying-your-credentials)
  - [List of utilities](#list-of-utilities)
    - [`fudan-grades`](#fudan-grades)
  - [Develop](#develop)
  - [See also](#see-also)
  - [Credits](#credits)

## Installation

### pipx

This is the recommended installation method.

```
$ pipx install fudan-utils
```

### [pip](https://pypi.org/project/fudan-utils/)

```
$ pip install fudan-utils
```

## Supplying your credentials

Set the `FUDAN_PID` and `FUDAN_PW` environment variables to your Fudan ID and password.

```bash
export FUDAN_PID=18309990001
export FUDAN_PW='123456verysecure!!!'
```

## List of utilities

### `fudan-grades`

Logs in to jwfw.fudan.edu.cn and get grades from the site.

```
$ fudan-grades -h

usage: fudan-grades [-h]

Get Fudan grades from jwfw

options:
  -h, --help  show this help message and exit


$ fudan-grades # don't forget to supply your credentials via environment variables

学年学期      课程代码      课程序号        课程名称     课程类别        学分     最终      绩点
-----------  ----------  -------------  ----------  ------------  ------  ------  ------
2022-2023 2  GTHB139999  GTHB139999.01  毕业论文     专业必修课程          6  F           0
```


## Develop

```
$ git clone https://github.com/tddschn/fudan-utils.git
$ cd fudan-utils
$ poetry install
```

## See also

- https://github.com/tddschn/fudan-jwc-news

## Credits

- https://github.com/FDUCSLG/pafd-automated for reverse engineering the login process