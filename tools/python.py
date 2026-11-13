from log import 日志
from fastmcp import FastMCP
import subprocess
import sys

mcp = FastMCP('python')

@mcp.tool()
def python(python_script: str) -> dict:
    '''你可以执行python脚本'''
    p = subprocess.run(
        [sys.executable, '-c', python_script],
        capture_output=True, text=True,
    )
    result = p.stdout + '\n' + p.stderr

    日志.信息(f'[Python] execute script: {python_script}, result: {result}')
    return {'success': True, 'result': result}

mcp.run(transport='stdio')
    