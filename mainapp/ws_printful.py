
import requests

class Printful():
    def __init__(self):
        self.api_key = "JU77AP8F3AmeZLzzt7r5z9hfh3SnJkaCovpSZ29FABiHLtoUWVvHbEi1XOOk3aCD"
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
            'client_id': 'app-8219094',
            'client_secret': self.api_key,
            'code': 'SF3smWPcWvInV8duOwEA39V1oUkaoxZ9jKpkPrNC',
        }

        response = requests.post(url, params=params).json()
        '''
        {'access_token': '0wmQFp7GHGxrdZGxddsq0vWv77QXzFfSx1fURs54', 'expires_at': 1678224868, 'token_type': 'bearer', 'refresh_token': 'o4RwHJLSc0F9UosCUKBC7UDydINRAoo99AHNFCYCW5RR7oZrXDrwmDBPGO97'}
        '''
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
            'client_id': 'app-8219094',
            'client_secret': self.api_key,
            'refresh_token': refresh_token,
        }

        response = requests.post(url, params=params).json()
        print(response)


    def get_scopes(self):
        headers = {'Authorization': 'bearer '+ 'ulxHyMH1SvD461JaYEFeajjpgHQZ4mWApIHXM1jafHTdj9QWB0aCm3Oc6LFJ'}
        url = self.host_api + '/oauth/scopes'
        response = requests.get(url,  headers=headers, verify=False, timeout=100)
        print(response)

    '''
    {'access_token': 'I3gwoRSobZarPflJ6X40kTS4C8Bl86XvCb9es9uS', 'expires_at': 1678235812, 'token_type': 'bearer', 'refresh_token': 'ulxHyMH1SvD461JaYEFeajjpgHQZ4mWApIHXM1jafHTdj9QWB0aCm3Oc6LFJ'}
    '''
    # 30 day valid token refresh xDHrC2NxEvQDI1NMnqld7HJmGOlBL8ZvuMJZOaCEPYRJybPGa8NJOLUWIojI
    #                   access KSswjbopXMORS4rLpCwSAfZwTGLK35XdtFM5cPrt