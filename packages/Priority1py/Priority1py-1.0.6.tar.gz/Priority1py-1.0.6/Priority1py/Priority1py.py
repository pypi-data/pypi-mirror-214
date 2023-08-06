from Priority1py.request import req_send
from Priority1py.strings import Endpoint, Crud, Accessorial, IDType, Details
# from request import req_send
# from strings import Endpoint, Crud, Accessorial, IDType, Details
import json
from datetime import datetime

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

        # test for no shipments found
        if 'No shipments found' in res_json:
            raise Exception('No shipments found matching that ID')

        # parse json for status list
        try:
            list = res_json['shipments'][0][target]

            return list
        
        except KeyError:
            return 'Bad '
        
    
    def get_full_tracking(self, identifier:str, identifiertype:str):
        ''' get full list of tracking for the shipment '''
        if identifiertype not in IDType:
            raise Exception('Invalid identifier type. Allowed targets:\n IDType.PO, IDType.BOL, IDType.PRO, IDType.EXT, IDType.CUST_REF, IDType.PICKUP_NUM')

        # get tracking statuses
        status_list = self.__get_items_from_tracking(identifier=identifier, identifiertype=identifiertype.value, target='trackingStatuses')
        return status_list


    def get_latest_tracking(self, identifier:str, identifiertype:str):
        ''' get the latest tracking update '''
        if identifiertype not in IDType:
            raise Exception('Invalid identifier type. Allowed targets:\n IDType.PO, IDType.BOL, IDType.PRO, IDType.EXT, IDType.CUST_REF, IDType.PICKUP_NUM')


        # get tracking statuses
        status_list = self.__get_items_from_tracking(identifier=identifier, identifiertype=identifiertype.value, target='trackingStatuses')

        # init emptpy dates list
        dates = [datetime(year=2023, month=1, day=1)] * len(status_list)

        # find latest tracking from list
        for i, j in enumerate(status_list):
            # extract time and date
            date = j['timeStamp'][:10]
            time = j['timeStamp'][11:16]

            # create datetime objects
            dt = datetime(year=int(date[:4]), month=int(date[5:7]), day=int(date[8:10]), hour=int(time[:2]), minute=int(time[3:5]))
            dates[i] = dt

        # get index of latest date from list of datetimes
        latest = dates.index(max(dates))

        # return the status at that index
        return status_list[latest]
        
        

    def get_shipment_details(self, indentifier:str, identifiertype:str, target:str):
        ''' get the current details of a shipment '''

        if identifiertype not in IDType:
            raise Exception('Invalid identifier type. Allowed targets:\n IDType.PO, IDType.BOL, IDType.PRO, IDType.EXT, IDType.CUST_REF, IDType.PICKUP_NUM')


        if target not in Details:
            raise Exception('Invalid target. Allowed targets:\n Details.STATUS, Details.CARRIER, Details.CARRIER_CODE')
        
        status = self.__get_items_from_tracking(identifier=indentifier, identifiertype=identifiertype.value, target=target.value)
        return status


    def get_identifier(self, identifier:str, identifiertype:str, target:str) -> str:
        ''' get P1 identifier number '''
        if identifiertype not in IDType:
            raise Exception('Invalid identifier type. Allowed targets:\n IDType.PO, IDType.BOL, IDType.PRO, IDType.EXT, IDType.CUST_REF, IDType.PICKUP_NUM')

        if target not in IDType:
            raise Exception('Invalid target type. Allowed targets:\n IDType.PO, IDType.BOL, IDType.PRO, IDType.EXT, IDType.CUST_REF, IDType.PICKUP_NUM')


        # get identifiers list
        id_list  = self.__get_items_from_tracking(identifier=identifier, identifiertype=identifiertype.value, target='shipmentIdentifiers')
        
        # find the target identifier by type
        for i in id_list:
            if i['type'] == target.value:
                return i['value']

        return f'No identifiers of type {target.value} found.'


