import unittest
from src.tweetscrapper.TweetManagers import *
from src.tweetscrapper.AuthorizationManager import AuthorizationManager

auth_header = AuthorizationManager("api_keys.json").get_bearer_token()
max_results = 10
lang = "pl"


class TestTweetManagers(unittest.TestCase):
    def test_get_tweets_by_hashtag(self):
        hashtag = "Za Tuska"
        data, meta = get_json_tweets_by_hashtag(auth_header, hashtag, max_results, lang)

        self.assertIsInstance(data, list)
        self.assertEqual(len(data) != 0, True)

        self.assertIsInstance(meta, dict)
        self.assertEqual(len(meta) != 0, True)

    def test_get_tweets_by_acc_name(self):
        acc_name = "DoRzeczy_pl"
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

    def test_get_conversation_ids(
        self,
    ):  # this could fail, no sample file with conversation id in repo
        path_to_json = r"E:\coding\pythonnew\tweet-manager\data2.json"
        conversation_ids = get_conversation_ids(path_to_json)
        self.assertIsInstance(conversation_ids, list)
        self.assertEqual(len(conversation_ids) != 0, True)

    def test_merge_jsons(self):
        path_to_jsons = r"E:\coding\pythonnew\tweet-manager\data\outputs"
        json_output = merge_jsons(path_to_jsons, "merged.json")
        self.assertEqual(json_output, True)
