''' constant strings used '''
from enum import Enum

class Endpoint(Enum):
    def __str__(self):
        return self.value
    LTL_RATE_QUOTE = '/v2/ltl/quotes/rates/'
    LTL_SHIPMENT_STATUS = '/v2/ltl/shipments/status/'


class Crud(Enum):
    def __str__(self):
        return self.value
    POST = 'POST'
    GET = 'GET'


class Accessorial(Enum):
    def __str__(self):
        return self.value
    GUARANTEED_5PM = 'GUR'
    DELIV_APPT = 'APPT'
    LIFT_GATE_DELIV = 'LGDEL'
    LTD_ACCESS_DELIV = 'LTDDEL'
    RES_DELIV = 'RESDEL'


class IDType(Enum):
    def __str__(self):
        return self.value
    PRO = 'PRO'
    BOL = 'BILL_OF_LADING'
    CUST_REF = 'CUSTOMER_REFERENCE'
    PICKUP_NUM = 'PICKUP'
    PO = 'PURCHASE_ORDER'
    EXT = 'EXTERNAL'

class Details(Enum):
    def __str__(self):
        return self.value
    CARRIER = 'carrierName'
    CARRIER_CODE = 'carrierCode'
    STATUS = 'status'
