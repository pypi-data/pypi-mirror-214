# YOLOv5 Installable Package

Packaged [ultralytics/yolov5](https://github.com/ultralytics/yolov5)

Inspired from https://github.com/fcakyon/yolov5-pip.

## Build Package
Build wheel file:
```bash
pip install build
python -m build
```

## Install with prebuilt package
Package-built has uploaded to pypi and just install with the command:
```bash
pip install yolov5-utils
```

### General imports
Insert `yolov5_utils.yolov5.` prefix when importing modules `models` and `utils`.
For example: 
```python
from yolov5_utils.yolov5.models.common import DetectMultiBackend
```

## Authors
**Msclock** - msclock@qq.com  - [Github account](https://github.com/msclock)
