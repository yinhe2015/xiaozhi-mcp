import sys
import os
sys.path.append(os.path.join(os.path.expanduser('~'), 'disk-d', 'pylib'))

from 日志 import 控制台日志
日志 = 控制台日志(输出=sys.stderr)