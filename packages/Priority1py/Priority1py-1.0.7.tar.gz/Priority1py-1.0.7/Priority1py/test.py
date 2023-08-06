from Priority1py import Priority1py
from strings import IDType, Details

if __name__ == '__main__':
    test = Priority1py('b80ebbe6-d4d7-48ce-ba19-3686d455eac4')
    
    ext = test.get_latest_tracking('DEN2211', IDType.PO)
    print(ext)