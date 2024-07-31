import os
import requests
from ChessPosition import ChessPosition
from logger import log

api_auth = os.environ.get("cf_api_key")

CF_URL = "https://us-central1-pedregosa-sb.cloudfunctions.net/knightpath-calculate"

def calculate_moves(source: str,target: str,operation_id:str)->None:
    """
        Function that sends request for knight moves to be calculated async
    """
    
    headers = {
        "Authorization": api_auth
    }
    
    res = requests.post(
            CF_URL, 
            json={
                'source':source,
                'target':target,
                'operation_id': operation_id
                },
            headers=headers,
            timeout=10
        )
    
    if res.status_code != 200:
        log(f"Reponse failure form calculating moves request. Status: {res.status_code} Message: {res.content}")
   
    



    