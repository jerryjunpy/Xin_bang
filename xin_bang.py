# coding: utf-8
from Xin_bang.utils import user_agent, config, md5_password
import time
import requests
from Xin_bang.utils.log import get_logger
import random
import hashlib
from w3lib.html import remove_tags
import jsonpath
import datetime
from requests.adapters import HTTPAdapter

logger = get_logger(__name__)



class XinbangSpider(object):

    def __init__(self):
        self.title_hash = list()
        self.account = ''
        self.password = ''
        self.session = requests.session()
        # self.session.headers = {"User_Agent": user_agent.UserAgent(mobile_ua=True)}
        # # 超时自动重新请求3次
        # max_retries = 3
        # adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        # self.session.mount('http://', adapter)
        # self.session.mount('https://', adapter)
        self.session.keep_alive = False

    def is_login(self):
        """
        判断是否可以用本地的cookies登录
        :return:
        """
        try:
            with open("XinbangCookies.txt", "r")as f:
                cookies = f.read()
            cookies = eval(cookies)
            cookie = "; ".join((key + "=" + value) for key, value in cookies.items())
            self.session.headers.update({"Cookie": cookie})

            usercenter_url = "https://www.newrank.cn/xdnphb/common/account/get"
            link = "/xdnphb/common/account/get?AppKey=joker"
            data = None
            nonce, xyz = md5_password.get_data(link, data)

            params = {
                "nonce": nonce,
                "xyz": xyz
            }
            response = self.session.post(usercenter_url, data=params)
            if response.json().get("value") == -999:
                # logger.info(f"Cookies已失效,新榜登录失败，headers={self.session.headers} data={params}")
                return False
            else:
                # logger.info(f"使用本地Cookies登录新榜成功, headers={self.session.headers} data={params}")
                return True
        except:
            # logger.info(f"Cookies已失效,新榜登录失败, headers={self.session.headers}")
            return False

    def login(self):
        data = {
            "flag": f"{round(time.time()*10000)}{str(random.random())[1:]}",
            "identifyCode": "",
            "password": md5_password.get_md5(md5_password.get_md5(self.password) + 'daddy'),
            "username": self.account,
        }
        link = "/xdnphb/login/new/usernameLogin?AppKey=joker&"
        nonce, xyz = md5_password.get_data(link, data)
        data.update(nonce=nonce, xyz=xyz)

        response = requests.post("https://data.newrank.cn/xdnphb/login/new/usernameLogin", data=data)

        if response.status_code == 200:
            result = jsonpath.jsonpath(response.json(), "$...msg")[0]
            if result == "登录成功":
                token = jsonpath.jsonpath(response.json(), "$...token")[0]

                cookies = {"name": self.account,
                           "token": token,
                           "useLoginAccount": "true"
                           }
                requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)
                with open("XinbangCookies.txt", 'w')as f:  # 将cookies保存到本地
                    f.write(str(cookies))
                return True

            else:
                # logger.error(f"新榜登录失败, headers={self.session.headers} data={data}")
                return False

    def main_crawler(self):
        first_keywords_list = ['贷款', '房地产']
        for key in first_keywords_list:
            params = {
                "category": "",
                "containAdd": key,
                "containOr": "",
                "eliminate": "",
                "endDate": "",
                "keywords": "",
                "orderBy": "1",  # 按时间排序
                "original": "0",
                "pageNumber": "1",
                "rankName": "",
                "searchType": "0",
                "startDate": "",
                "video": "0",
                "week": "1",
            }
            post_link = '/xdnphb/data/article/search?AppKey=joker&'
            post_nonce, post_xyz = md5_password.get_data(post_link, params)
            params.update(nonce=post_nonce, xyz=post_xyz)

            query_url = 'https://data.newrank.cn/xdnphb/data/article/search'

            try:
                res = self.session.post(query_url, data=params)

                result = res.json()

                if result.get("value") == -999:  # 登录失败
                    pass
                else:
                    article_list = jsonpath.jsonpath(result, "$...datas")[0]
                    for article in article_list:
                        published_time = jsonpath.jsonpath(article, "$...publicTime")[0]
                        # last_day = (now - timedelta(days=1)).strftime('%Y-%m-%d')  # 昨天的日期

                        if published_time > datetime.date.today().strftime("%Y-%m-%d"):  # 当天的日期:

                            article_url = jsonpath.jsonpath(article, "$...url")[0]
                            article_title = remove_tags(jsonpath.jsonpath(article, "$...title")[0])
                            hl = hashlib.md5()
                            hl.update(article_title.encode(encoding='utf-8'))
                            title_sign = hl.hexdigest()
                            if title_sign in self.title_hash:
                                continue
                            self.title_hash.append(title_sign)  # 根据标题去重

                            information_data = {
                                "platform_name": "新榜",
                                "title_sign": title_sign,
                                "published_time": published_time,
                                "article_title": article_title,
                                "article_url": article_url,
                                "create_time": int(time.time())
                            }
                            print(information_data)
                            logger.info(f"title_sign={title_sign} 保存结果, 数据保存成功")

            except Exception:
                logger.exception(f"{'GET'} headers={self.session.headers} data={params}")


def main():
    q = XinbangSpider()
    if q.is_login():  # 判断是否可以用cookie登录
        q.main_crawler()
    else:
        if q.login():
            q.main_crawler()

if __name__ == '__main__':

    main()
