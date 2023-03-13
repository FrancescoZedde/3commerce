
import requests

class Printful():
    def __init__(self):
        self.api_key = ""
        self.host = 'https://www.printful.com'
        self.host_api = 'https://www.api.printful.com'

    def make_header(access_token):
        headers = {'Authorization':'Bearer '+access_token}
        return headers
        #-H 'Authorization: Bearer smk_GN0I1Os3OdfqzjJnTOWn1wlbqqq2Y2Pc10TS'

    '''
    POST request to https://www.printful.com/oauth/token page with the following parameters:
    grant_type=authorization_code
    client_id={clientId}
    client_secret={clientSecret}
    code={authorizationCode}
    '''
    def get_access_token(self):
        url = self.host + '/oauth/token'

        params = {
            'grant_type': 'authorization_code',
            'client_id': '',
            'client_secret': self.api_key,
            'code': '',
        }

        response = requests.post(url, params=params).json()
        
        print(response)
        return response['access_token'], response['refresh_token']


    '''
     To refresh tokens you must make a POST request to https://www.printful.com/oauth/token with the parameters:    
    grant_type=refresh_token
    client_id={clientId}
    client_secret={clientSecret}
    refresh_token={refreshToken}
    '''

    def refresh_token(self, refresh_token):
        url = self.host + '/oauth/token'

        params = {
            'grant_type': 'refresh_token',
            'client_id': '',
            'client_secret': self.api_key,
            'refresh_token': refresh_token,
        }

        response = requests.post(url, params=params).json()
        print(response)


    def get_scopes(self):
        headers = {'Authorization': 'bearer '+ ''}
        url = self.host_api + '/oauth/scopes'
        response = requests.get(url,  headers=headers, verify=False, timeout=100)
        print(response)

    # 30 day valid token refresh xDHrC2NxEvQDI1NMnqld7HJmGOlBL8ZvuMJZOaCEPYRJybPGa8NJOLUWIojI
    #                   access KSswjbopXMORS4rLpCwSAfZwTGLK35XdtFM5cPrt