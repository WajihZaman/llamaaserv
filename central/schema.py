from pydantic import BaseModel
from uuid import UUID



class UserQuery(BaseModel):
    uid: UUID | None = UUID("d4123af6-f0c4-4707-a5b1-9428839b42f3")
    emp_no: int | None = 12345
    convo_id: str | None = "conversation code"
    msg: str | None = "Introduce yourself"
