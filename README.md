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
