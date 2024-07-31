import os
import functions_framework
from logger import log
from ChessPosition import ChessPosition
from service import (
    calculate_shortest_path, 
    chess_to_cartesian, 
    cartesian_to_chess,
    update_operation
    )

auth_key = os.environ.get("auth_key")

@functions_framework.http
def knightpath_calculate(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        payload:
            source: string
            target: string
            operation_id: string
    Returns:
        Success string - 200
    """
    headers = request.headers

    auth = headers.get("Authorization")

    if auth != auth_key:
        return "Invalid Auth", 401
    
    request_json = request.get_json(silent=True)
  
    
    source = request_json.get("source")
    target = request_json.get("target")
    operation_id = request_json.get("operation_id")

    try:
        start_pos = ChessPosition(notation=source)
        end_pos = ChessPosition(notation=target)
    except ValueError as e:
        return "Required field source or target is missing or incorret",400
    
    path = []
    
    num_of_moves, path = calculate_shortest_path(
        start_pos.to_coords(),
        end_pos.to_coords()
    )
    
    chess_path = ""
    
    for idx, pos in enumerate(path):
        chess_pos = cartesian_to_chess(pos)
        
        if idx == 0:
            chess_path = chess_path + chess_pos
        else:
            chess_path = chess_path + ":" + chess_pos

    
    log(f"Number of moves {num_of_moves} Shortes path: {path} \n {chess_path}")
    

    res = update_operation(
        source,
        target,
        operation_id,
        num_of_moves,
        chess_path
        )
    

    return "Success", 200
