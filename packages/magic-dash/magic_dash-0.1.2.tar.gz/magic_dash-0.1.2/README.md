<p align="center">
	<img src="./magic_dash/templates/magic-dash/assets/imgs/logo.svg" height=100></img>
</p>
<h1 align="center">magic-dash</h1>
<div align="center">

[![Pyhton](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](./setup.py)
[![GitHub](https://shields.io/badge/license-MIT-informational)](https://github.com/CNFeffery/magic-dash/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/magic-dash.svg?color=dark-green)](https://pypi.org/project/magic-dash/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

</div>

命令行工具，用于快捷生成一系列标准[Dash](https://github.com/plotly/dash)应用工程模板。

## 目录

[安装](#install)<br>
[使用](#usage)<br>
[内置模板列表](#template-list)<br>

<a name="install" ></a>

## 安装

```bash
pip install magic-dash -U
```

<a name="usage" ></a>

## 使用

### 查看内置项目模板

```bash
magic-dash list
```

### 生成指定项目模板

- 默认生成到当前路径

```bash
magic-dash create --name magic-dash
```

- 指定生成路径

```bash
magic-dash create --name magic-dash --path 目标路径
```

### 查看当前`magic-dash`版本

```bash
magic-dash --version
```

### 查看命令说明

```bash
magic-dash --help

magic-dash list --help

magic-dash create --help
```

<a name="template-list" ></a>

## 内置模板列表

```bash
内置Dash应用项目模板：

- magic-dash    基础多页面应用模板
- simple-tool    单页面工具应用模板
```