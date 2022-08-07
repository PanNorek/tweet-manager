from src.tweetscrapper.AuthorizationManager import AuthorizationManager
from src.tweetscrapper.QueryBuilder import QueryBuilder



def main():
    """ Main program """
    #get authorization token from json file
    authorize = AuthorizationManager('api_keys.json').get_bearer_token()
    query = QueryBuilder('pl', 10).get_by_hashtag('Izrael')
    
    print(authorize)
    print(query)
    











if __name__ == '__main__':
    main()