from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from backend.api.models.request_model import CommandRequest
from backend.api.models.response_model import CommandListResponse, CommandSingleResponse
from backend.data.data_models import Command
from backend.data.engine import get_db
#hello world!

# Prefix: "/commands"
command_router = APIRouter(tags=["Commands"])


@command_router.get("/", response_model=CommandListResponse)
def get_commands(db: Session = Depends(get_db)):
    """
    Gets all the items

    @return Returns a list of commands
    """
    query = select(Command)
    items = db.exec(query).all()
    return {"data": items}


@command_router.post("/", response_model=CommandSingleResponse)
def create_command(payload: CommandRequest, db: Session = Depends(get_db)): 
    """
    Creates an item with the given payload in the database and returns this payload after pulling it from the database 

    @param payload: The data used to create an item
    @return returns a json object with field of "data" under which there is the payload now pulled from the database 
    """
    # TODO:(Member) Implement this endpoint
    try:
        request = Command(**payload.model_dump())
        db.add(request)
        db.commit()
        db.refresh(request)
        return {"data":request}
    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))



@command_router.delete("/{id}", response_model=CommandListResponse)
def delete_command(id: int, db: Session = Depends(get_db)):
    """
    Deletes the item with the given id if it exists. Otherwise raises a 404 error.

    @param id: The id of the item to delete
    @return returns the list of commands after deleting the item
    """
    # TODO:(Member) Implement this endpoint
    query = select(Command).where(Command.id == id)
    removed_item = db.exec(query).first()

    if removed_item is None:
        raise HTTPException(status_code=404, detail="Item does not exist.")
    
    db.delete(removed_item)
    db.commit()
    
    query_all = select(Command).where(Command.id != id)
    items = db.exec(query_all).all()
    return {"data" : items}