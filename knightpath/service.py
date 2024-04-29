import os
import requests
from logger import log

api_auth = os.environ.get("cf_api_key")

CF_URL = "https://us-central1-pedregosa-sb.cloudfunctions.net/knightpath-calculate"

def calculate_moves(source,target,operation_id):
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
        return False
    
    return True

def check_cases(chess_pos):
    """
        Checks cases for chess board positions
        Example:
            A5
            
            Position 0 must be alpha and not greater than H
            Position 1 must be numeric and not greater than 7
    """
    try:
        x_pos = chess_pos[0]
        y_pos = chess_pos[1]
        
        
        if not x_pos.isalpha() or not y_pos.isdigit():
            return False
        
        if x_pos > "H":
            return False
        
        if int(y_pos) > 8 or int(y_pos)<1: 
            return False
    except (IndexError, AttributeError):
        return False
    
    return True
    