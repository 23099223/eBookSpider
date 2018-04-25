import threading
import datetime
import com.spider.Spiders as spd
import com.config.RuleConfig as RuleConfig
import com.config.PropertyConfig as PropertyConfig
import com.spider.SpiderUtil as spdu
import logging
import redis
import json
import os


# 队列锁
# L = threading.Lock()
# # txturl队列
# # TXT_URL_Q = queue.Queue()
# # txt章节url队列
# SECTION_URL_Q = queue.Queue()


class Master(threading.Thread):
    def __init__(self, threadname, rc):
        threading.Thread.__init__(self, name=threadname)
        self.MAIN_URL = rc.MAIN_URL
        self.CODE = rc.CODE
        self.TXT_URL_XPATH = rc.TXT_URL_XPATH
        self.TXT_PAGE_URL_XPATH = rc.TXT_PAGE_URL_XPATH

    def run(self):
        r = redis.Redis(host="localhost", port="6379", password="Redis@123!")
        page_url_l = [RuleConfig.MAIN_URL]
        page = self.MAIN_URL
        while True:
            html = spd.gethtml(page, self.CODE)
            info = spd.getinfo(html, self.TXT_URL_XPATH)
            page = spd.getinfo(html, self.TXT_PAGE_URL_XPATH)
            logging.info("info的长度： %s" % len(info))
            for url_dict in info:
                r.lpush("TXT_URL_LIST1", json.dumps(url_dict, ))
            page = RuleConfig.REFERER + page[0][1]
            if page in page_url_l:
                logging.info(" %s 结束！" % self.getName())
                break
            page_url_l.append(page)


class Section(threading.Thread):
    def __init__(self, threadname, rc, master):
        threading.Thread.__init__(self, name=threadname)
        self.CODE = rc.SECTION_CODE
        self.SECTION_URL_PATH = rc.SECTION_URL_PATH
        self.master = master
        self.SECTION_URL = rc.SECTION_URL
        self.TXT_NAME = rc.TXT_NAME

    def run(self):
        r.delete("SECTION_URL_LIST_2")
        txt_name = self.TXT_NAME
        html = spd.gethtml(self.SECTION_URL, self.CODE)
        page = spd.getinfo(html, self.SECTION_URL_PATH)
        logging.info(" 章节数： %s" % len(page))
        logging.info(" 章节数： %s" % page)
        spdu.store(page + [self.TXT_NAME])
        for line in page:
            line.append(txt_name)
            InRedisList(line).start()


class Content(threading.Thread):
    '''
    :param threadname: 线程名称
    :param rc: 规则配置
    :param sections: section线程集合，旨在判断章节线程是否结束
    :param code: 页面编码，默认utf
    '''

    def __init__(self, threadname, rc, sections):
        threading.Thread.__init__(self, name=threadname)
        self.CONTENT_XPATH = rc.CONTENT_XPATH
        self.SECTIONS = sections
        self.CODE = rc.CONTENT_CODE
        self.REFERER = rc.REFERER

    def run(self):
        while True:
            string = r.rpop('SECTION_URL_LIST_2')
            if string is None and sec_flag:
                logging.warning("SECTION_URL_LIST_2队列为空且SECTION线程结束,%s停止..." % self.getName())
                break
            if string is None:
                continue
            string = json.loads(string)
            section_name, sectione_url, txt_name = string[0], self.REFERER + string[1], string[2]
            html = spd.gethtml(sectione_url, self.CODE)
            page = spd.getinfo(html, self.CONTENT_XPATH, True)
            page = [page] + [txt_name, spdu.replace_spec(section_name)]
            logging.info("%s爬取：%s" % (self.getName(), section_name))
            spdu.write_section(page)


class InRedisList(threading.Thread):
    def __init__(self, ll):
        threading.Thread.__init__(self, name="insert")
        self.ll = ll

    def run(self):
        r.lpush("SECTION_URL_LIST_2", json.dumps(self.ll))


logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.DEBUG)
starttime = datetime.datetime.now()
logging.info(" 爬取开始")
pool = redis.ConnectionPool(host='localhost', port=6379, password="Redis@123!")
r = redis.Redis(connection_pool=pool)
# master_thread = Master('master线程', RuleConfig, 'gbk')
# master_thread.start()
# logging.info(master_thread.getName() + " 还活着" if master_thread.is_alive() else " 死了")
# master_thread.join()

# section_thread = Section('section线程-%s', RuleConfig, "", 'gbk')
# section_thread.start()
# section_thread.join()
sec_flag = False
section_threads = []
for i in range(PropertyConfig.SECTION_WORK_MAX):
    section_thread = Section('section线程-%s' % str(i + 1), RuleConfig, "")
    logging.info(" %s 开始！" % section_thread.getName())
    section_thread.start()
    section_threads.append(section_thread)

content_threads = []
for i in range(PropertyConfig.CONTENT_WORK_MAX):
    content_thread = Content('content线程-%s' % str(i + 1), RuleConfig, section_threads)
    logging.info(" %s 开始！" % content_thread.getName())
    content_thread.start()
    content_threads.append(content_thread)
#
for i in section_threads:
    i.join()
sec_flag = True
for i in content_threads:
    i.join()

# master_thread.join()
logging.info(" 爬取结束")

data = []

with open('%s/%s/目录.json' % (PropertyConfig.TXT_PATH, RuleConfig.TXT_NAME), 'r', encoding='utf-8') as f:
    data = json.load(f)
print(len(data[0:-1]))
print(data[0:-1])
with open("%s/%s/%s.txt" % (PropertyConfig.TXT_PATH, RuleConfig.TXT_NAME, RuleConfig.TXT_NAME), 'w',
          encoding='utf-8') as txt:
    for line in data[0:-1]:
        section = line[0]
        # section = spdu.replace_spec(section)
        with open("%s/%s/%s.json" % (PropertyConfig.TXT_PATH, RuleConfig.TXT_NAME, section), 'r', encoding='utf-8') as sec:
            content = json.load(sec)
            logging.info("写入 %s 章节" % section)
            txt.write(section + '\r\n' + content + '\r\n')

# 写入txt后自动删除json文件
os.system('rm -f %s/%s/*.json' % (PropertyConfig.TXT_PATH, RuleConfig.TXT_NAME))
endtime = datetime.datetime.now()
logging.info("此次爬取所费时间：%s" % (endtime - starttime))
