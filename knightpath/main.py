import functions_framework
import uuid
import os

from ChessPosition import ChessPosition
from operation import get_operation
from service import calculate_moves
import threading


auth_key = os.environ.get("auth")

@functions_framework.http
def knight_moves(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        GET - Operation Object
            source
            target
            shorestPath
            numOfMoves
        POST - operationId
    """
    headers = request.headers

    auth = headers.get("Authorization")

    if auth != auth_key:
        return "Invalid Auth", 401

    http_method = request.method
    
    if http_method == "GET":

        request_args = request.args
        
        operation_id = request_args.get("operationId")

        if not operation_id:
            return "Invalid Request: operationId is required",400
        
        res = get_operation(operation_id)
        
        if not res:
            return f"Operation Id {operation_id} Not Found", 404
        
        return res, 200
        
    elif http_method == "POST":

        request_json = request.get_json(silent=True)
        
        source = request_json.get("source")
        target = request_json.get("target")
        
        if not source:
            return "Missing required field source", 400
        if not target:
            return "Missing required field target", 400
        


        try:
            start_pos = ChessPosition(notation=source)
            end_pos = ChessPosition(notation=target)
        except ValueError as e:
            return f"Invalid source or target position: {str(e)}",400
  
        
        operation_id = str(uuid.uuid4())
        
        
        # Make it Async!
        t = threading.Thread(target=calculate_moves,args=(start_pos.to_notation(),end_pos.to_notation(),operation_id))
        t.start()

        
        return {"operation_id": operation_id}, 200
        
    elif http_method != "OPTIONS":
        return "Invalid HTTP Method Type", 405
    



