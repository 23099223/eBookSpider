from selenium import webdriver
import time
from lxml import etree
import os

driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--load-images=false'])
# driver.set_window_size(1280, 2400)
driver.get('http://www.booktxt.net/xiaoshuodaquan/')
content = driver.page_source
print(content)
selector = etree.HTML(content)
txt_name_list = selector.xpath('//div[@class="novellist"]/ul/li/a/text()')
print(txt_name_list)
driver.close()
# 防止driver.close()没有结束phantomjs进程
os.system("ps -ef | grep phantomjs | awk '{print $2}' | xargs kill -9")
