from src.AuthorizationManager.AuthorizationManager import AuthorizationManager






def main():
    """ Main program """
    #get authorization token from json file
    authorize = AuthorizationManager('api_keys.json').get_bearer_token()


    print(authorize)












if __name__ == '__main__':
    main()