from buaa_open_source_22371550_test_package1 import fetch_page
from bs4 import BeautifulSoup

def parse_page(url):
    """ 获取网页内容并解析网页，提取标题和正文 """
    # 从包 1 获取网页内容
    html = fetch_page(url)
    if not html:
        return "Error", "Failed to fetch page"
    
    # 解析网页内容
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else "No title"
    paragraphs = soup.find_all('p')
    content = " ".join(p.get_text() for p in paragraphs)
    return title, content
