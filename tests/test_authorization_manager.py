import unittest


from src.AuthorizationManager.AuthorizationManager import *


class TestAuthorizationManager(unittest.TestCase):
    # test_json_filename = r'E:\coding\pythonnew\newscrapper\your_api_keys_sample.json'
    test_json_filename = '../your_api_keys_sample.json'
    instance = AuthorizationManager()

    def test_access_token(self):
        self.assertEqual(self.instance.access_token, 'verylongstringhere')
     
    def test_get_access_token_secret(self):
        self.assertEqual(self.instance.access_token_secret, 'verylongstringhere')
    
    def test_get_bearer_token(self):
        self.assertEqual(self.instance.get_bearer_token(), {'Authorization': 'Bearer veryverylongstringhere'})
    
    def test_get_api_key(self):
        self.assertEqual(self.instance.api_key,'longstringhere')
    
    def test_get_api_secret(self):   
        self.assertEqual(self.instance.api_secret,'verylongstringhere')

        