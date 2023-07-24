#!/usr/bin/env python
# encoding: utf-8
"""
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2020/4/14
"""
import json
from scrapy import Spider
from scrapy.http import Request
from spiders.common import parse_tweet_info, parse_long_tweet


class TweetSpider(Spider):
    """
    用户推文数据采集
    """
    name = "tweet_spider"
    base_url = "https://weibo.cn"

    def start_requests(self):
        """
        爬虫入口 2023.7.16-pages:664
         INFO: Crawled 3662 pages (at 16 pages/min), scraped 6626 items (at 22 items/min)
        """
        # 这里user_ids可替换成实际待采集的数据
        user_ids = ['3937348351']
        for user_id in user_ids:
            url = f"https://weibo.com/ajax/statuses/mymblog?uid={user_id}&page=2051"
            yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': 2051})

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        tweets = data['data']['list']
        for tweet in tweets:
            item = parse_tweet_info(tweet)
            del item['user']
            if item['isLongText']:
                url = "https://weibo.com/ajax/statuses/longtext?id=" + item['mblogid']
                yield Request(url, callback=parse_long_tweet, meta={'item': item})
            else:
                yield item
        if tweets:
            user_id, page_num = response.meta['user_id'], response.meta['page_num']
            page_num += 1
            url = f"https://weibo.com/ajax/statuses/mymblog?uid={user_id}&page={page_num}"
            yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num})
