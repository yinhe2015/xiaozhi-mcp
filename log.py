import sys
import os
sys.path.append(os.path.join(os.path.expanduser('~'), 'disk-d', 'pylib'))

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
keys_dir = os.path.join(base_dir, 'keys')

from 日志 import 控制台日志
日志 = 控制台日志(输出=sys.stderr)