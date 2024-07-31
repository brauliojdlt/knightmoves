
import collections
from firebase_admin import exceptions
from logger import log
import google.cloud.firestore
from firebase_admin import initialize_app, firestore, credentials
from flask import abort

app = initialize_app(options={'projectId':'pedregosa-sb'})
firestore_client: google.cloud.firestore.Client = firestore.client()


def chess_to_cartesian(chess_notation):
    """
        Converts Chess coordinates to cartestian
        Example: A2 -> (0,1) 
    """
    try:
        x_value = chess_notation[0]
        y_value = chess_notation[1]
        
        x=0
        y=int(y_value) -1
        
        
        if x_value == "A":
            x = 0
        elif x_value == "B":
            x = 1
        elif x_value == "C":
            x = 2
        elif x_value == "D":
            x = 3
        elif x_value == "E":
            x = 4
        elif x_value == "F":
            x = 5
        elif x_value == "G":
            x = 6
        elif x_value == "H":
            x = 7
        
        return (x, y)

    except IndexError as e:
        log(f"Index error converting chess to cartesian {str(e)}")
        return False
    
def cartesian_to_chess(cartesian_notation):
    """
        Converts Cartesian to chess
        Example:  (0,1) -> A2
    """
    try:
        x_value = cartesian_notation[0]
        y_value = cartesian_notation[1]
    except IndexError as e:
        log(f"Index error converting cartesian to chess {str(e)}")
        return False
    
    x = ""
    
    if x_value == 0:
        x = "A"
    elif x_value == 1:
        x = "B"
    elif x_value == 2:
        x = "C"
    elif x_value == 3:
        x = "D"
    elif x_value == 4:
        x = "E"
    elif x_value == 5:
        x = "F"
    elif x_value == 6:
        x = "G"
    elif x_value == 7:
        x = "H"
        
    y = str(int(y_value)+1)
    
    return x+y
    
    

def calculate_shortest_path(source_val: tuple, target_val: tuple):
    """
    BFS path finding function
    Inputs:
        source - coordinate tuple
        target - coordinate tuple
    Returns:
        Number of moves - int
        Shortest Path - array of tuples
    """
    moves = [
        (2,1),
        (2,-1),
        (-2,1),
        (-2,-1),
        (1,2),
        (1,-2),
        (-1,2),
        (-1,-2)
    ]

    # Initialize the queue with the source position and path
    queue = collections.deque([(source_val, [source_val])])
    visited = set([source_val])

    while queue:
        current_pos, path = queue.popleft()

        if current_pos == target_val:
            return len(path)-1, path

        for move in moves:
            new_source = (current_pos[0]+move[0], current_pos[1]+move[1])

            if 0 <= new_source[0] <= 7 and 0 <= new_source[1] <= 7 and new_source not in visited:
                visited.add(new_source)
                new_path = path + [new_source]
                queue.append((new_source, new_path))

    return -1, []  # Return -1 for path length and an empty list for the path if no path is found  





def update_operation(source:str, target:str, operation_id:str, num_of_moves: int, shortest_path: str) -> str:
    """
        Creates knight moves object in firebase
    """
    knight_moves = {
        "starting": source,
        "ending": target,
        "numberOfMoves": num_of_moves,
        "shortestPath": shortest_path,
        "operationId":operation_id
    }
    
    try:
        firestore_client.collection("knight_moves").document(operation_id).set(knight_moves)
        
    except exceptions.FirebaseError as e:
        log(f"Exception occurreed while create operation in db {str(e)}")
        abort(500,description=f'Internal error when updating shortest path')

    
    return operation_id
    
    