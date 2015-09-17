import subprocess
import os

resource_root = os.path.dirname(__file__)
rcc_cmd = [
    'pyside-rcc',
    '-o',
    '../psforms/resource.py',
    'resource.qrc',
]
subprocess.call(rcc_cmd, cwd=resource_root)
