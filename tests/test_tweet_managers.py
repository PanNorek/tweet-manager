import unittest
from src.tweetscrapper.TweetManagers import *

auth_header = AuthorizationManager('api_keys.json').get_bearer_token()
max_results = 10
lang = 'pl'

class TestTweetManagers(unittest.TestCase):
    def test_get_tweets_by_hashtag(self):
        hashtag = 'Za Tuska'
        data, meta = get_json_tweets_by_hashtag(auth_header, hashtag, max_results, lang)

        self.assertIsInstance(data, list)
        self.assertEqual(len(data) != 0, True)

        self.assertIsInstance(meta, dict)
        self.assertEqual(len(meta) != 0, True)

    def test_get_tweets_by_acc_name(self):
        acc_name = 'DoRzeczy_pl'
        data, meta = get_tweets_by_acc_name(auth_header, acc_name, max_results, lang)

        self.assertIsInstance(data, list)
        self.assertEqual(len(data) != 0, True)

        self.assertIsInstance(meta, dict)
        self.assertEqual(len(meta) != 0, True)
    
    def test_get_replies(self):
        conversation_id = 1556279401582661633
        data, meta = get_replies(auth_header, conversation_id, max_results, lang)

        self.assertIsInstance(data, list)
        self.assertEqual(len(data) != 0, True)

        self.assertIsInstance(meta, dict)
        self.assertEqual(len(meta) != 0, True)

