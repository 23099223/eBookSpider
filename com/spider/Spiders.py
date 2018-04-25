import urllib.error
import http.cookiejar
from lxml import html
import time
import com.config.RuleConfig as RuleConfig
import com.spider.SpiderUtil as SpiderUtil
import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.DEBUG)


# 页面爬取
def gethtml(url, code='utf-8'):
    '''

    :param url: 需爬取的页面
    :param code: 页面编码
    :return:
    '''
    cjar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    opener.addheaders = [(key, value) for key, value in SpiderUtil.get_headers(RuleConfig.REFERER).items()]
    urllib.request.install_opener(opener)
    try:
        html = opener.open(url, timeout=15).read().decode(code, errors='ignore')
    except Exception as e:
        logging.error('gethtml爬取 %s %s %s' % (url, '异常: ', str(e)))
        time.sleep(2)
        html = gethtml(url, code)
    return html


def getinfo(page, xpath, flag=False):
    '''

    :param page: 要解析的页面
    :param xpath: 为达到通用,此参数表示筛选标签的xpath
    :param flag: True:获取页面信息;False:获取页面URL
    :return:
    '''
    etree = html.etree
    selector = etree.HTML(page)
    for line in xpath:
        info = "".join(selector.xpath(line)).replace(u'\xa0', u' ') if flag else list(map(
            lambda x: [SpiderUtil.replace_spec(''.join(x.xpath('text()'))),
                       str(''.join(x.xpath('@href')).replace(u'\r\n\t\t\t', ''))],
            selector.xpath(line)))
        if flag and len("".join(info).replace(u'\xa0', u' ').replace(u'\r\n', '')) > 50:
            break
    return info

if __name__ == "__main__":
    print(gethtml(RuleConfig.SECTION_URL, code='gbk'))
    # page = gethtml('https://www.ybdu.com/xiaoshuo/0/140/', 'gbk')
    # print(getinfo(page, RuleConfig.SECTION_URL_PATH, False))
