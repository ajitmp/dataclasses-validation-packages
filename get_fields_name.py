from pydantic import BaseModel
from typing import List, Optional

class NoteSchema(BaseModel):
    title: str
    content: str
    tags: List[str]
    user_id: int
    created_at: Optional[str] = None

# Get the list of field names from the Pydantic model
field_names = list(NoteSchema.model_fields.keys())


print(field_names)

