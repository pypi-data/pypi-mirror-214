''' classes used for sending requests to P1 API '''
import requests, json

class req_send():
    ''' class to send url '''
    def __init__(self, key:str, base_url:str='https://api.priority1.com'):
        self.base_url = base_url
        self.key = key

    
    def send_req(self, endpoint:str, payload:dict, request:str) -> str:
        ''' sends a request to P1 and return the string
            takes in endpoint string and json data for
            request body '''
        
        headers = {
            'X-API-KEY' : self.key,
            'accept' : 'application/json',
            'Content-type' : 'application/json'
        }
        
        # print(headers)
        # print(payload)

        url = self.base_url + endpoint.value

        data = json.dumps(payload)

        # print(url)

        try:
            result = requests.request(request.value, url=url, headers=headers, data=data)
            return result.text
        
        except requests.exceptions.HTTPError as e:
            raise Exception('HTTP Error occurred.')
        

    def set_base_url(self, url:str) -> str:
        ''' set new url '''
        self.base_url = url
        return self.base_url
    

    def set_key(self, key:str) -> str:
        ''' set new key '''
        self.key = key
        return self.key