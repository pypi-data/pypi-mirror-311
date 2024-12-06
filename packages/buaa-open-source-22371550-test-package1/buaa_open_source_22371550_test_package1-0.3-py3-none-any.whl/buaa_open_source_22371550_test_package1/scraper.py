# scraper.py
import requests
import chardet

def fetch_page(url):
    """ 获取指定 URL 的网页内容 """
    try:
        response = requests.get(url)
        response.raise_for_status()

        # 使用 chardet 检测网页的编码
        detected_encoding = chardet.detect(response.content)
        response.encoding = detected_encoding['encoding']

        return response.text
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

def test_fetch_page():
    """ 测试 fetch_page 功能 """
    url = "https://www.baidu.com"  # 示例 URL
    html_content = fetch_page(url)
    assert html_content is not None, "Failed to fetch page"
    print(f"Fetched content for {url}")
    return html_content
