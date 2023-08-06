# vscode-icons
Django app to provide vscode icons for web application.

Please refer to [original author](https://marketplace.visualstudio.com/items?itemName=vscode-icons-team.vscode-icons) for more detail.

## Installation

Following command will help to install the package.

```bash
pip install vscode-icons
```

## Setup

1. Add the app to **setting.py** file in **INSTALLED_APPS** section.

```python
INSTALLED_APPS = [
    ...
    'vscode_icons',
]
```

## Usage

```python
from vscode_icons.vscode import VSCodeIcons

vsi = VSCodeIcons()

# Getting file path
file_name = 'image.png'
file_icon_path = vsi.findFileIcon(file_name)
print(f'File Icon:\t {file_icon_path}')

# Getting directory path
dir_name = 'Documents'
dir_icon_path = vsi.findDirectoryIcon(dir_name)
print(f'Directory Icon:\t {dir_icon_path}')
```

#### Output

```bash
File Icon:       vscode_icons/icons/file_type_image.svg
Directory Icon:  vscode_icons/icons/default_folder.svg
```

## Author

**Tahir Rafique**

## Releases

| Date      | Version | Summary       |
| --------- | ------- | ------------- |
| 15-Jun-23 | v1.0.0  | Initial build |

