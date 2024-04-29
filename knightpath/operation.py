import uuid
from firebase_admin import exceptions
from firebase_init import firestore_client
from logger import log

def get_operation(operation_id):
    """
        Function that returns an operation document
        
        Input: (str) Operation Id 
        Returns: (dict) Operation dict
    """

    doc_ref = firestore_client.collection("knight_moves").document(operation_id) 
    doc = doc_ref.get()
    
    if doc.exists:
        return doc.to_dict()
    else:
        return False

