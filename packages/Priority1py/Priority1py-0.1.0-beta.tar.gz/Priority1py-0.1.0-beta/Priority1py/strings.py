''' constant strings used '''
from enum import Enum

class Endpoint(Enum):
    LTL_RATE_QUOTE = '/v2/ltl/quotes/rates'
    LTL_SHIPMENT_STATUS = '/v2/ltl/shipments/status'


class Crud(Enum):
    POST = 'POST'
    GET = 'GET'


class Accessorial(Enum):
    GUARANTEED_5PM = 'GUR'
    DELIV_APPT = 'APPT'
    LIFT_GATE_DELIV = 'LGDEL'
    LTD_ACCESS_DELIV = 'LTDDEL'
    RES_DELIV = 'RESDEL'


class IDType(Enum):
    PRO = 'PRO'
    BOL = 'BILL_OF_LADING'
    CUST_REF = 'CUSTOMER_REFERENCE'
    PICKUP_NUM = 'PICKUP'
    PO = 'PURCHASE_ORDER'
    EXT = 'EXTERNAL'