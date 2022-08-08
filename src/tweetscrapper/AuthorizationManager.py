import json
from pathlib import Path
import os




class AuthorizationManager:
    '''Simple class to get the keys  from a json file'''
    # path_to_json_file:str = r'E:\coding\pythonnew\tweet-manager\your_api_keys_sample.json'
    

    def __init__(self, json_filename:str = 'your_api_keys_sample.json'):
        """
        Args:
            json_filename (str, optional): name of json file with stored Tweeter API keys. Defaults to 'your_api_keys_sample.json'.
        """
        try:
            with open(os.path.join(Path(__file__).parents[2], json_filename),'r') as file:
                keys = json.load(file)
                self._bearer_token = keys['Bearer_Token']
                self._api_key = keys['API_Key']
                self._api_secret = keys['API_Key_Secret']
                self._access_token = keys['Access_Token']
                self._access_token_secret = keys['Access_Token_Secret']
                self._app_id = keys['App_ID']
        except Exception as e:
            print(e)
            
    # getters for the keys
    
    def get_bearer_token(self):
        return {'Authorization': 'Bearer ' + self._bearer_token} 

    @property
    def api_key(self):
        return self._api_key if self._api_key else None
    
    @property
    def api_secret(self):
        return self._api_secret if self._api_secret else None
    
    @property
    def access_token(self):
        return self._access_token if self._access_token else None
    
    @property
    def access_token_secret(self):
        return self._access_token_secret if self._access_token_secret else None
    
    @property
    def app_id(self):
        return self._app_id if self._app_id else None
    
    @property
    def json_filename(self):
        return self.path_to_json_file
    
    @json_filename.setter
    def json_filename(self,value):
        self.path_to_json_file = value

    def get_keys(self)-> dict:
        """
        Getter for all Twitter Api keys
    
            Returns:
         (dict):  All keys you get on Twitter API.
        """
        return {'Bearer_Token':self.bearer_token,
                'API_Key':self.api_key,
                'API_Secret':self.api_secret,
                'Access_Token':self.access_token,
                'Access_Token_Secret':self.access_token_secret,
                'App_ID':self.app_id}