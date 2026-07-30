import subprocess
import shutil
import json
import sys
import os

with open('MCP_ENDPOINT.txt', 'r', encoding='utf-8') as f:
    MCP_ENDPOINT = f.read().strip()

base_dir = os.getcwd()
mcp_pipe_path = os.path.join(base_dir, 'mcp_pipe.py')

tools_dir = os.path.join(base_dir, 'tools')
run_dir = os.path.join(base_dir, 'run')
os.makedirs(tools_dir, exist_ok=True)
os.makedirs(run_dir, exist_ok=True)

mcp_config_file = os.path.join(run_dir, 'mcp_config.json')
mcp_config_list = {}

with open(os.path.join(run_dir, 'log.py'), 'w', encoding='utf-8') as f:
    f.write(f'''\
''')

for file in os.listdir(tools_dir):
    if file.endswith('.py'):
        tgt_dir = os.path.join(run_dir, file)
        shutil.copy(os.path.join(tools_dir, file), tgt_dir)

        name = file[:-3]
        mcp_config_list[name] = {
            'type': 'stdio',
            'command': sys.executable,
            'args': ['-m', name]
        }

if not mcp_config_list:
    print('No tool found')
    exit(1)
with open(mcp_config_file, 'w', encoding='utf-8') as f:
    json.dump({'mcpServers': mcp_config_list}, f)

env = os.environ.copy()
env['MCP_ENDPOINT'] = MCP_ENDPOINT

mcp_pipe_process = subprocess.Popen(
    [sys.executable, mcp_pipe_path],
    env=env,
    cwd=run_dir,
)
mcp_pipe_process.wait()