from pydantic import BaseModel

class GreetRequest(BaseModel):
    name:str
    withError:bool

class GreetResponse(BaseModel):
    reply:str