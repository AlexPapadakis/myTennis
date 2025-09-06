from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError


def execute_query_and_handle_errors(query, entity_not_found):
    try:
        result = query()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
    if result is None:
        raise HTTPException(status_code=404, detail=entity_not_found+" not found")
    
    print("Query executed successfully.")
    return result

