# dataclasses-validation-packages

In any Python project or in other language we need to use same fields name at various places throughout the project processing pipeline. Such requirement is omnipresence and often leads to errors, debugging time and code breaking at runtime. So, how we can keep the fields/attributes/column names consistent throughout the project. (to avoid typos, mismatch names etc) Let understand the problem with an example:

Suppose, my project involves using data scraping for data collection and then store and serve it through back-end infrastructure (web application or API).

    Now, if, i use Scrapy for data scraping then i have to create Item() with required data fields (suppose: book_title, author, pages and price), later same fields name should be used in spiders for data scraping which may get saved as JSON .

    The json file may be dump to a database directly (to populate data for an application) then the table/s needs to be created in database , possibly with same names to avoid errors.

    Similarly, if Django is used as backend, then the model and serializer will also have these fields name, so again we need to repeat same fields names.

    if we want to do some data operation, suppose with pandas then either we can import JSON or may create dataframe manually (repeating the fields name).

We can see that in one project, we need to repeat the fields name multiple time. Variations in name may or maynot lead to errors or issues. However, being consistent with name is good and safe with big projects.

So, what is the best possible ways to achieve it? When, i started working on this many python modules pops up, but most of them are heavy and offers many features that is either supported in individual packages/framework and integrating those with external packages create conflicts and unnecessary loads on the project.

I want some thing very simple, like just text file etc . Note: I am not asking for any type hint or data validations etc. just want to have consistent field name. for example, student_name, name, stu_name, should be just anyone throughout the project.

I tried many package offering class based features for creating datamodels. Like, Pydantic, Itemloader, marshmallow, attrib , etc.

For example, following code gives use fields name that can be used in other part of the project but this seems like overdoing by using Pydantic just to get fields name:

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

pythondjangoapiscrapyschema


# 📦 Consistent Field Definitions in Python Data Pipelines

### Comparing `dataclasses`, `Pydantic`, `Marshmallow`, `SQLModel`, and `ItemAdapter` for Scraping & Backend Safety

---

## 📌 Problem Statement

In most real-world Python projects—especially those involving **data scraping → storage → API/backend → analytics**—the same field names must be reused across multiple layers:

* Scrapy `Item`
* JSON exports
* Database tables
* Django models & serializers
* Pydantic schemas
* Pandas DataFrames
* API responses

Example fields:

```
book_title, author, pages, price
```

If you accidentally use:

```
title
bookTitle
book_name
```

…you introduce silent bugs, runtime errors, or hard-to-debug inconsistencies.

### The Core Requirement

We want:

* ✅ Consistent field names across the project
* ✅ Minimal overhead
* ❌ No heavy validation if not required
* ❌ No unnecessary framework lock-in

This README compares practical approaches using:

* `dataclasses`
* `Pydantic`
* `Marshmallow`
* `SQLModel`
* `ItemAdapter`

---

# 🏗 Typical Scraping → Backend Pipeline

```
Scrapy → JSON → Database → Django/FastAPI → Pandas
```

Every layer repeats the same field definitions.

The question:

> What is the safest and simplest way to define fields once and reuse everywhere?

---

# 1️⃣ Marshmallow – Serialization Focus

Marshmallow is schema-driven and good for transforming & serializing data.

```python
from marshmallow import Schema, fields
from datetime import date

class ArtistSchema(Schema):
    name = fields.Str()

class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
    artist = fields.Nested(ArtistSchema())

bowie = dict(name="David Bowie")
album = dict(artist=bowie, title="Hunky Dory", release_date=date(1971, 12, 17))

schema = AlbumSchema()
result = schema.dump(album)
```

Output:

```python
{
  'artist': {'name': 'David Bowie'},
  'release_date': '1971-12-17',
  'title': 'Hunky Dory'
}
```

### ✔ Pros

* Strong serialization/deserialization control
* Good for API transformation
* Nested schemas supported

### ❌ Cons

* Requires explicit field declaration
* Overkill if you only need field names

---

# 2️⃣ Pydantic – Validation + Field Introspection

Pydantic provides runtime validation and structured models.

```python
from pydantic import BaseModel
from typing import List, Optional

class NoteSchema(BaseModel):
    title: str
    content: str
    tags: List[str]
    user_id: int
    created_at: Optional[str] = None

field_names = list(NoteSchema.model_fields.keys())
print(field_names)
```

Output:

```
['title', 'content', 'tags', 'user_id', 'created_at']
```

### Validation Example

```python
from pydantic import ValidationError

external_data = {'id': 'not an int', 'tastes': {}}

try:
    User(**external_data)
except ValidationError as e:
    print(e.errors())
```

Structured validation errors are returned automatically.

### ✔ Pros

* Automatic validation
* Field name extraction
* Data coercion
* Excellent FastAPI integration

### ❌ Cons

* Heavy dependency if only used for field names
* Adds validation logic even when not needed

---

# 3️⃣ SQLModel – DB + Validation Unified

`SQLModel` combines SQLAlchemy + Pydantic.

```python
from sqlmodel import Field, SQLModel, create_engine

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
```

Insert data:

```python
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)
```

Query:

```python
from sqlmodel import Session, select

with Session(engine) as session:
    statement = select(Hero).where(Hero.name == "Spider-Boy")
    hero = session.exec(statement).first()
```

### ✔ Pros

* Single source for DB schema + validation
* Clean ORM
* Avoids duplication between models and schemas

### ❌ Cons

* Heavy if scraping-only
* Tightly coupled to database layer

---

# 4️⃣ Python `dataclasses` – Minimal & Lightweight

If you only need consistent fields without validation:

```python
from dataclasses import dataclass

@dataclass
class InventoryItem:
    name: str
    price: float
    stock: int
```

Simple, clean, zero extra dependencies.

### ✔ Pros

* Built-in (Python standard library)
* Extremely lightweight
* Clean field declaration

### ❌ Cons

* No built-in validation
* No automatic serialization

---

# 5️⃣ ItemAdapter – Universal Abstraction Layer

`ItemAdapter` provides a unified interface across:

* dict
* dataclass
* Pydantic model
* attrs
* Scrapy Item

```python
from itemadapter import ItemAdapter

obj = InventoryItem(name='foo', price=20.5, stock=10)

adapter = ItemAdapter(obj)
print(adapter["name"])
adapter["name"] = "bar"
```

Nested example:

```python
@dataclass
class Price:
    value: int
    currency: str

@dataclass
class Product:
    name: str
    price: Price

item = Product("Stuff", Price(42, "UYU"))
adapter = ItemAdapter(item)
print(adapter.asdict())
```

Supported adapters:

```
ScrapyItemAdapter
DictAdapter
DataclassAdapter
AttrsAdapter
PydanticAdapter
```

### ✔ Pros

* Abstracts underlying data type
* Perfect for scraping pipelines
* Lightweight
* Flexible

### ❌ Cons

* No validation by itself
* Requires structured object beforehand

---

# 🔍 So What Is the Best Approach?

It depends on your goal.

| Goal                        | Recommended   |
| --------------------------- | ------------- |
| Only consistent field names | `dataclass`   |
| Validation required         | `Pydantic`    |
| DB + validation unified     | `SQLModel`    |
| Serialization control       | `Marshmallow` |
| Scrapy pipeline abstraction | `ItemAdapter` |

---

# 🧠 Minimalist Strategy (Recommended for Simplicity)

If you **only want consistent field names** without validation:

### Option 1 – Dataclass as Single Source of Truth

```python
@dataclass
class Book:
    title: str
    author: str
    pages: int
    price: float
```

Then reuse:

* Scrapy
* JSON dump
* DB insertion
* Django model mapping
* Pandas columns

Extract fields:

```python
from dataclasses import fields
field_names = [f.name for f in fields(Book)]
```

---

### Option 2 – Plain Constant File (Ultra Lightweight)

`fields.py`

```python
BOOK_FIELDS = [
    "title",
    "author",
    "pages",
    "price"
]
```

Use everywhere:

```python
from fields import BOOK_FIELDS
```

This avoids heavy dependencies entirely.

---

# 🏁 Final Recommendation

If you do not require validation:

> **Use Python `dataclass` + optional `ItemAdapter` for pipeline consistency.**

If validation is critical (API, user input):

> Use `Pydantic` strategically, not everywhere.

Avoid introducing heavy schema frameworks purely to extract field names.

---

# 📚 Further Reading

* Python dataclasses vs attrs vs Pydantic
* Using Pydantic with Django
* Schema-driven design in scraping pipelines

---

# 🎯 Key Takeaway

Field name consistency is a **design discipline**, not just a tooling issue.

The cleanest solution is often:

```
One single source of truth for field definitions
```

Everything else should reference that source—not redefine it.

---

If needed, this can be extended into:

* A production-ready scraping template
* Django + Scrapy integration blueprint
* Clean architecture data pipeline template
