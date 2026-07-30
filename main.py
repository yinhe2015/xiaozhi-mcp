from dotenv import load_dotenv
import subprocess
import shutil
import json
import sys
import os

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))
mcp_pipe_path = os.path.join(base_dir, 'mcp_pipe.py')

tools_dir = os.path.join(base_dir, 'tools')
run_dir = os.path.join(base_dir, 'run')
os.makedirs(tools_dir, exist_ok=True)
os.makedirs(run_dir, exist_ok=True)

append_mcp_config_file = os.path.join(base_dir, 'append_mcp_config.json')
mcp_config_file = os.path.join(run_dir, 'mcp_config.json')
try:
    with open(append_mcp_config_file, 'r', encoding='utf-8') as f:
        mcp_config_str = f.read()
    for key, value in os.environ.items():
        mcp_config_str = mcp_config_str.replace('{{' + key + '}}', value)
    mcp_config = json.loads(mcp_config_str)
except FileNotFoundError:
    mcp_config = {}
if 'mcpServers' not in mcp_config:
    mcp_config['mcpServers'] = {}

shutil.copy(os.path.join(base_dir, 'log.py'), os.path.join(run_dir, 'log.py'))

for file in os.listdir(tools_dir):
    if file.endswith('.py'):
        tgt_dir = os.path.join(run_dir, file)
        shutil.copy(os.path.join(tools_dir, file), tgt_dir)

        name = file[:-3]
        mcp_config['mcpServers'][name] = {
            'type': 'stdio',
            'command': sys.executable,
            'args': ['-m', name]
        }

if not mcp_config['mcpServers']:
    print('No tool found')
    exit(1)
with open(mcp_config_file, 'w', encoding='utf-8') as f:
    json.dump(mcp_config, f)

mcp_pipe_process = subprocess.Popen(
    [sys.executable, mcp_pipe_path],
    cwd=run_dir,
)
mcp_pipe_process.wait()