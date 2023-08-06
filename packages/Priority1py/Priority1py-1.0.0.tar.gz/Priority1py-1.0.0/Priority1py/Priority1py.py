from Priority1py.request import req_send
from Priority1py.strings import Endpoint, Crud, Accessorial, IDType
# from request import req_send
# from strings import Endpoint, Crud, Accessorial, IDType
import json

class Priority1py():
    ''' API helper class '''

    def __init__(self, key:str):
        self.key = key
        self.req = req_send(self.key)   # request sender obj


    def __get_items_from_tracking(self, identifier:str, identifiertype:str, target:str):
        ''' return list of passed in target values '''

        payload = {
            'identifierType' : identifiertype,
            'identifierValue' : identifier
        }

        # send request and convert to json 
        res_str = self.req.send_req(endpoint=Endpoint.LTL_SHIPMENT_STATUS, payload=payload, request=Crud.POST)
        res_json = json.loads(res_str)
        print(res_json)

        # test for no shipments found
        if 'No shipments found' in res_json:
            raise Exception('No shipments found matching that ID')

        # parse json for status list
        try:
            list = res_json['shipments'][0][target]

            return list
        
        except KeyError:
            return 'Bad '
    

    def get_latest_tracking(self, identifier:str, identifiertype:str):
        ''' get the latest tracking update '''

        # get tracking statuses
        status_list = self.__get_items_from_tracking(identifier=identifier, identifiertype=identifiertype.value, target='trackingStatuses')

        latest_status = status_list[0]
        
        return {
            'timestamp' : latest_status['timeStamp'],
            'status' : latest_status['status'],
            'statusreason' : latest_status['statusReason'],
            'location' : latest_status['city'] + ', ' + latest_status['state']
        }


    def get_identifier(self, identifier:str, identifiertype:str, target:str) -> str:
        ''' get P1 identifier number '''

        # get identifiers list
        id_list  = self.__get_items_from_tracking(identifer=identifier, identifiertype=identifiertype, target='shipmentIdentifiers')
        
        # find the target identifier by type
        for i in id_list:
            if i['type'] == target:
                return i['value']



