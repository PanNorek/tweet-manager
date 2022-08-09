from src.tweetscrapper.QueryBuilder import QueryBuilder
# from src.tweetscrapper.AuthorizationManager import AuthorizationManager
from typing import Tuple
import requests
import collections

# auth_header = AuthorizationManager('api_keys.json').get_bearer_token()
# max_results = 10
# lang = 'pl'


class ConnectionError(Exception):
    """Raised when the TweetManager cannot handle specified query"""
    pass


# TODO: add documentation to functions


def flatten(d, parent_key='', sep='_'):
    """_summary_

    Args:
        d (_type_): _description_
        parent_key (str, optional): _description_. Defaults to ''.
        sep (str, optional): _description_. Defaults to '_'.

    Returns:
        _type_: _description_
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_json_tweets_by_hashtag(
    auth_header: dict,
    hashtag: str,
    max_results: int,
        lang: str) -> Tuple[list, dict]:
    """_summary_

    Args:
        hashtag (str): _description_

    Raises:
        ConnectionError: _description_

    Returns:
        Tuple[list, dict]: _description_
    """

    url = QueryBuilder(lang, max_results).get_by_hashtag(hashtag)

    response = requests.get(url, headers=auth_header)

    if response.status_code != 200:
        print('Error for hashtag: {}!'.format(hashtag))
        print(f'Response failed with code: {response.status_code}')
        raise ConnectionError

    # Flatten nested dictionary
    data = [flatten(tweet_data) for tweet_data in response.json()["data"]]

    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

    # with open('meta.json', 'w', encoding='utf-8') as f:
    #     json.dump(response.json()["meta"], f, ensure_ascii=False, indent=4)
    return data, response.json()["meta"]


def get_tweets_by_acc_name(
    auth_header: dict,
    name: str,
    max_results: int,
        lang: str) -> Tuple[list, dict]:
    """_summary_

    Args:
        auth_header (dict): _description_
        name (str): _description_
        max_results (int): _description_
        lang (str): _description_

    Raises:
        ConnectionError: _description_

    Returns:
        Tuple[list, dict]: _description_
    """
    url = QueryBuilder(lang, max_results).get_by_acc_name(name)

    response = requests.get(url, headers=auth_header)

    if response.status_code != 200:
        print('Error for account name: {}!'.format(name))
        print(f'Response failed with code: {response.status_code}')
        raise ConnectionError

    # Flatten nested dictionary
    data = [flatten(tweet_data) for tweet_data in response.json()["data"]]

    # with open('data2.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

    # with open('meta2.json', 'w', encoding='utf-8') as f:
    #     json.dump(response.json()["meta"], f, ensure_ascii=False, indent=4)
    return data, response.json()["meta"]


def get_replies(
    auth_header: dict,
    conversation_id: str,
    max_results: int,
        lang: str) -> Tuple[list, dict]:
    """_summary_

    Args:
        auth_header (dict): _description_
        conversation_id (str): _description_
        max_results (int): _description_
        lang (str): _description_

    Raises:
        ConnectionError: _description_

    Returns:
        Tuple[list, dict]: _description_
    """
    url = (QueryBuilder(lang, max_results)
           .get_replies_from_tweet(
                conversation_id,
                max_results))

    response = requests.get(url, headers=auth_header)

    if response.status_code != 200:
        print('Error for conversation_id {}!'.format(conversation_id))
        print(f'Response failed with code: {response.status_code}')
        raise ConnectionError

    # Flatten nested dictionary
    data = [flatten(tweet_data) for tweet_data in response.json()["data"]]

    return data, response.json()["meta"]


def get_conversation_ids(data: list) -> list:
    """_summary_

    Args:
        path_to_json (str): _description_

    Returns:
        list: _description_
    """

    return [tweet['conversation_id'] for tweet in data]


def extract_text():
    raise NotImplementedError


def anonymize_mentions():
    raise NotImplementedError
