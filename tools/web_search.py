from log import 日志, keys_dir
from fastmcp import FastMCP
from bs4 import BeautifulSoup
import requests
import os

with open(os.path.join(keys_dir, 'tavily.txt'), 'r', encoding='utf-8') as f:
    tavily_key = f.read().strip()

mcp = FastMCP('web_search')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

@mcp.tool()
def web_search(keyword: str, limit: int = 5) -> dict:
    '''
    关键词网络搜索，获取网页列表（标题、摘要、url）
    Args:
        keyword: 要搜索的关键词
        limit: 返回结果最大条数，默认5条
    Returns:
        dict 包含success与搜索结果列表
    '''
    # ========== 这里是演示占位 ==========
    # 生产环境请替换为 searxng / serpapi / 其他搜索API调用
    # 下面为模拟返回示例，你需要替换成真实搜索接口调用
    results = [
        {
            'title': f'【{keyword}】相关网页 {i+1}',
            'summary': f'关于 {keyword} 的摘要信息，简单描述网页内容片段',
            'url': f'https://example-{i+1}.com?q={keyword}'
        }
        for i in range(limit)
    ]

    日志.信息(f'[WebSearch] keyword={keyword}, limit={limit}, hit {len(results)} items')
    return {
        'success': True,
        'keyword': keyword,
        'results': results
    }

@mcp.tool()
def web_fetch(url: str) -> dict:
    '''
    获取指定网页链接的正文文本内容
    Args:
        url: 需要读取内容的网页地址
    Returns:
        dict，包含网页标题、提取后的正文、是否成功
    '''
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # 清理: 移除 脚本, 样式
        for bad in soup(['script', 'style']):
            bad.decompose()

        page_title = soup.title.get_text(strip=True) if soup.title else None
        plain_text = soup.get_text(separator='\n', strip=True)

        日志.信息(f'[WebFetch] url={url}, title={page_title[:40]}')
        return {
            'success': True,
            'url': url,
            'page_title': page_title,
            'content': plain_text
        }
    except Exception as e:
        err_msg = str(e)
        日志.错误(f'[WebFetch] url={url} fetch failed: {err_msg}')
        return {
            'success': False,
            'url': url,
            'error': err_msg
        }

if __name__ == '__main__':
    mcp.run(transport='stdio')