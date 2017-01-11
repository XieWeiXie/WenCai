#!/usr/bin/env python
# encoding: utf-8

"""
@author: paul.xie
@software: PyCharm
@time: 2017/1/10 10:52
"""
from pprint import pprint
import pymongo.errors
import requests
import logging
from random import choice
from docs.config import USER_AGENT
from lxml import etree
from docs.kword import keys
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MyLogger(object):
    def __init__(self):
        pass


class WenCaiCrawler(object):

    category = "wencai_stock"

    def __init__(self):
        self.base_url = "http://www.iwencai.com/stockpick/"
        self.user_agent = choice(USER_AGENT)
        self.query_hint = "http://www.iwencai.com/stockpick/query-hint-list?sessionId=944281484026057085&q={}"
        self.recommend_url = "http://www.iwencai.com/asyn/search"
        self.params = {
            "queryType":"stock",
            "app":"qnas",
            "qid":None,
            "q": None
        }
        self.keywords= keys
        self.collection = MongoClient("192.168.100.20", 27017)["ada"]["wencai"]
        self.cookies = {
            'PHPSESSID': '6ae9hlk3ipf4fg3vpjh0t1tu12',
            'guideState': '1',
            'cid': '6ae9hlk3ipf4fg3vpjh0t1tu121484015615',
            'ComputerID': '6ae9hlk3ipf4fg3vpjh0t1tu12170110+103335',
        }

        self.headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': self.user_agent,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'http://www.iwencai.com/stockpick/',
            'X-Requested-With': 'XMLHttpRequest',
            'Proxy-Connection': 'keep-alive',
        }
        pass

    def fetch(self, url, data=None):
        html = requests.session()
        self.params["q"] = data
        try:
            if data!=None:
                self.params["w"] = data
                response = html.get(url, headers=self.headers, params=self.params, cookies=self.cookies)
                return response
            else:
                response = html.get(url, headers=self.headers,cookies=self.cookies)
                return response
        except requests.ConnectionError as e:
            print e

    def question_parse(self):
        """
        首页问题关键字
        :return:
        """
        response = self.fetch(self.base_url,data=None)
        if response:
            document = etree.HTML(response.content)
            new_query = document.xpath('//div[contains(@class,"area_item")][4]//div[contains(@class,"layout_item")][1]//div[contains(@class,"col_query")]')
            classic_query = document.xpath('//div[contains(@class,"area_item")][4]//div[contains(@class,"layout_item")][2]//div[contains(@class,"col_query")]')
            new_items = [one.xpath('dl//a/text()') for one in new_query]
            classic_items = [one.xpath('dl//a/text()') for one in classic_query]
            new_items.extend(classic_items)
        return new_items

    def association_query(self, keyword):
        """
        由关键字得出的联想词
        :param keyword:
        :return:
        """
        url = self.query_hint.format(keyword)
        response = self.fetch(url).json()
        data_items = response['data']['docs']
        return data_items

    def recommend_query(self, keyword):
        response = self.fetch(self.recommend_url, keyword).json()
        recommend_items = response["suggest"]["templ"]
        # print (recommend_items)
        recommened_doc = etree.HTML(recommend_items)
        doc = recommened_doc.xpath('//li//a/text()')
        return doc

    def push_to_db(self):
        pass

    def main(self):
        keywords = []
        new, classic = self.question_parse()
        keywords.extend(new)
        keywords.extend(classic)
        keywords.extend(self.keywords)
        for item in keywords[30:]:
            for i in range(len(item)):
                d = item[0:i+1]
                association_info = {"kw":d, "asscociation":{}}
                collection_item = self.association_query(d)
                for m in collection_item:
                    association_info["asscociation"][m] = []
                if collection_item:
                    for one in collection_item:
                        recommend_item = self.recommend_query(one)
                        if recommend_item:
                            association_info["asscociation"][one]= recommend_item
                            # print association_info
                            print d, one
                if not association_info["asscociation"]:
                    continue
                try:
                    self.collection.insert_one(association_info)
                except pymongo.errors.DuplicateKeyError:
                    pass

if __name__=="__main__":
    A = WenCaiCrawler()
    A.main()
    # keywords = "股价低位且主力建仓"
    # B = A.recommend_query(keywords)
    # for one in B:
    #     print one