import unittest

# import selected elements, ex.:
from src.tweetscrapper.QueryBuilder import *


class TestQueryMaker(unittest.TestCase):
    instance = QueryBuilder(lang='pl')

    def test_url_builder_by_hashtag_11(self):
        hashtag = 'samplehashtag'
        self.assertEqual(self.instance.url_builder_by_hashtag_11(hashtag),
         'https://api.twitter.com/1.1/search/tweets.json?q=%23samplehashtag&lang=pl&sort_order=recency&tweet.fields=created_at&max_results=10&expansions=author_id')

    def test_get_by_hashtag(self):
        hashtag = 'samplehashtag'
        self.assertEqual(self.instance.get_by_hashtag(hashtag),
        'https://api.twitter.com/2/tweets/search/recent?query=%22samplehashtag%22++lang%3Apl&max_results=10&sort_order=recency&tweet.fields=conversation_id,created_at,public_metrics&expansions=author_id')

    def test_get_by_acc_name(self):
        acc_name = 'samplename'
        self.assertEqual(self.instance.get_by_acc_name(acc_name),
        'https://api.twitter.com/2/tweets/search/recent?query=from%3Asamplename+-is%3Areply+-is%3Aretweet&max_results=10&sort_order=recency&tweet.fields=conversation_id,created_at,public_metrics&expansions=author_id')

    def test_get_replies_from_tweet(self):
        conversation_id = 123123123123
        self.assertEqual(self.instance.get_replies_from_tweet(conversation_id),
        'https://api.twitter.com/2/tweets/search/recent?query=conversation_id%3A123123123123&max_results=10&sort_order=recency&tweet.fields=created_at,public_metrics&expansions=author_id')
        