# File Organizer

File Organizer is a Python tool that organizes files in a directory based on their extensions. It can sort files into categories like images, videos, audio, text files, and archives. The organization can be done either at a single level or with nested folders.

## Installation

You can install this package via pip:

```bash
pip install file-organizer
```

## Usage

You can use the tool by importing it into your script:

```python
from file_organizer import organize_files_by_extension

# Organize files with nested folder structure
organize_files_by_extension('path_to_directory', nested=True)

# Or use single-level organization
# organize_files_by_extension('path_to_directory', nested=False)

```
## License
This project is licensed under the MIT License.