from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import Optional, List
from enum import Enum

class Role(str, Enum):
    role_1 = "admin"
    role_2 = "aluna"
    role_3 = "instrutora"

# shared properties
class UserBase(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    role: Optional[List[Role]]