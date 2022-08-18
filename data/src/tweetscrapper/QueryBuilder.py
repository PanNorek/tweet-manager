import urllib.parse

#  https://developer.twitter.com/apitools/api?endpoint=%2F2%2Ftweets%2Fsearch%2Frecent&method=get
#  https://ceo.com.pl/ranking-popularnosci-polskich-politykow-na-twitterze-74439


# LANG = 'pl'
# urllib.parse.quote_plus(query)


class QueryBuilder:
    """
    This class is used to create the query for the Twitter API.

    """

    # more info about twitter api
    # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets

    def __init__(self, lang: str, count=10) -> None:
        self._lang = lang
        self.count = count

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, lang: str):
        self._lang = lang

    def url_builder_by_hashtag_11(self, hashtag: str, count: int = 10) -> str:
        """
        This method is used to build the url for the Twitter API 1.1.
        Args:
            hashtag: str - The hashtag to be searched
            count: int - The number of tweets to be returned
        Returns:
            str - The url for the Twitter API
        """
        base_url = "https://api.twitter.com/1.1/search/tweets.json"
        # add hashtag
        query = f"q={urllib.parse.quote_plus('#' + hashtag)}"
        # add language
        query += f"&lang={self.lang}"
        # add sort order
        query += "&sort_order=recency"
        # add tweet fields
        query += "&tweet.fields=created_at"
        # add max results
        query += f"&max_results={count}"
        # add expand
        query += "&expansions=author_id"

        # build the url
        url = base_url + "?" + query
        return url

    def get_by_hashtag(self, hashtag: str) -> str:
        """Generate an API request string by selecting a hashtag.

        Args:
            hashtag (str): hashtag or phrase to be found


        Returns:
            str: Complete url string to query for specified hashtag.
        """

        default_string = "https://api.twitter.com/2/tweets/search/recent?query="

        # quotes for exact phrase match
        specified_string = '"' + hashtag + '" '
        # add desired language
        specified_string += f" lang:{self.lang}"
        # convert an url string to safe characters
        specified_string = urllib.parse.quote_plus(specified_string)
        # add query filters
        specified_string += f"&max_results={self.count}&sort_order=recency&tweet.fields=conversation_id,created_at,public_metrics&expansions=author_id"

        return default_string + specified_string

    def get_by_acc_name(self, name: str) -> str:
        """Generate an API request string by selecting an user

        Args:
            name (str): Matches any Tweet from a specific user.
            The value can be either the username (excluding the @ character) or the user's numeric user ID.

        Returns:
            str: Complete url string to query for specified user.
        """

        default_string = "https://api.twitter.com/2/tweets/search/recent?query="
        specified_string = "from:" + name
        # get only 'original' tweets
        specified_string += " -is:reply -is:retweet"
        # convert an url string to safe characters
        specified_string = urllib.parse.quote_plus(specified_string)
        # add query filters
        specified_string += f"&max_results={self.count}&sort_order=recency&tweet.fields=conversation_id,created_at,public_metrics&expansions=author_id"

        return default_string + specified_string

    def get_replies_from_tweet(
        self, conversation_id: int, max_results: int = None
    ) -> str:
        """Generate an API request string that matches Tweets that share a common conversation ID.

        Args:
            conversation_id (int): single conversation ID
            max_results (int, optional): specify the maximum replies got by query,
             otherwise the number is set to class count property. Defaults to None.

        Returns:
            str: Complete url string to query for specified conversation ID.
        """
        if max_results is not None:
            count = max_results
        else:
            count = self.count

        default_string = "https://api.twitter.com/2/tweets/search/recent?query="
        specified_string = "conversation_id:" + str(conversation_id)
        # convert an url string to safe characters
        specified_string = urllib.parse.quote_plus(specified_string)
        # add query filters
        specified_string += f"&max_results={count}&sort_order=recency&tweet.fields=created_at,public_metrics&expansions=author_id"

        return default_string + specified_string
