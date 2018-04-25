import com.config.PropertyConfig as PropertyConfig
import random
import json
import os


class SpiderUtil(object):
    def __init__(self):
        self.USER_AGENT = PropertyConfig.USER_AGENT

    def getuser_agent(self):
        agent = random.choice(self.USER_AGENT)
        return agent


def get_headers(url=""):
    headers = {"User-Agent": random.choice(PropertyConfig.USER_AGENT),
               "Referer": url if url != "" else "https://www.baidu.com", "Connection": "keep-alive"}
    # print(headers)
    return headers


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def store(data):
    txt_path = "%s/%s" % (PropertyConfig.TXT_PATH, data[-1])
    print(txt_path)
    create_dir(txt_path)
    with open('%s/目录.json' % txt_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data))
        # json_file.readlines()


def write_section(data):
    txt_path = "%s/%s" % (PropertyConfig.TXT_PATH, data[1])
    create_dir(txt_path)
    with open('%s/%s.json' % (txt_path, data[2]), 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data[0]))


def replace_spec(spec_str):
    spec_str = spec_str.replace(u'?', '？').replace(u'*', '.').replace(u'"', '“').replace(u'/', '-').replace(u'|', '')
    return spec_str

# if __name__ == "__main__":
#     store([1, 2, 'test'])
# ua = SpiderUtil()
# h = get_headers()
# print(get_headers())
