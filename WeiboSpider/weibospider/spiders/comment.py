# encoding: utf-8
"""
"""
import json
from scrapy import Spider
from scrapy.http import Request
from spiders.common import parse_user_info, parse_time, url_to_mid

class CommentSpider(Spider):
    """微博评论数据采集 """

    '''f"https://weibo.com/2803301701/M1v1gpj3N#comment"
                       '''
    name = "comment"
    def start_requests(self):
        """爬虫入口"""
        tweet_ids = ['M1v1gpj3N']
        for tweet_id in tweet_ids:
            mid = url_to_mid(tweet_id)#https://weibo.com/2803301701/M1v1gpj3N#comment
            url =  f"https://weibo.com/ajax/statuses/buildComments?" \
                   f"is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count=20"
            yield Request(url, callback=self.parse, meta={'source_url': url})
    def parse(self, response, **kwargs):
        """网页解析"""
        data = json.loads(response.text)
        for comment_info in data['data']:
            item = self.parse_comment(comment_info)
            yield item
        if data.get('max_id', 0) != 0:
            url = response.meta['source_url'] + '&max_id=' + str(data['max_id'])
            yield Request(url, callback=self.parse, meta=response.meta)
    @staticmethod
    def parse_comment(data):
        """解析comment """
        item = dict()
        item['created_at'] = parse_time(data['created_at'])
        item['_id'] = data['id']
        item['like_counts'] = data['like_counts']
        item['ip_location'] = data['source']
        item['content'] = data['text_raw']
        item['comment_user'] = parse_user_info(data['user'])
        return item
