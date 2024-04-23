import pymongo 

from datetime import datetime
from beanie import Document, Indexed
from pydantic import Field

class User(Document):

    name: Indexed(str, unique=True)
    create_time: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = 'user'


class QAMsg(Document):
    user: str
    question_origin: str
    question_middleout: str
    answer: str = Field(default=None)
    created_time: datetime = Field(default_factory=datetime.now)
    updated_time: datetime = Field(default=None)

    class Settings:
        name = 'qa_msg'
        indexes = [
            [
                ("user", pymongo.ASCENDING),
                ("create_time", pymongo.DESCENDING),
            ]
        ]