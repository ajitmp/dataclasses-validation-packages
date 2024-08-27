from pydantic import BaseModel, Field
from itemadapter import ItemAdapter

class NoteModel(BaseModel):
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)
    user_id: int



# Create an instance of the Pydantic model
note = NoteModel(title="Sample Note", content="This is a sample note.", tags=["sample", "note"], user_id=1)

# Wrap the Pydantic model with ItemAdapter
adapter = ItemAdapter(note)

validated_note = NoteModel(**adapter.asdict())
print(validated_note)

# Get all field names from the adapted item
field_names = adapter.field_names()

print(field_names)


