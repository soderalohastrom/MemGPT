""" This module contains the data types used by MemGPT. Each data type must include a function to create a DB model. """
import uuid
from abc import abstractmethod
from typing import Optional, List
import numpy as np


from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, JSON
from sqlmodel import Field, Session, SQLModel, create_engine

from docarray.typing import NdArray


# Defining schema objects:
# Note: user/agent can borrow from MemGPTConfig/AgentConfig classes


class Record(SQLModel, table=True):
    """
    Base class for an agent's memory unit. Each memory unit is represented in the database as a single row.
    Memory units are searched over by functions defined in the memory classes
    """

    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    user_id: str
    agent_id: str
    text: str

    def to_record(self):
        # TODO: remove
        return self


class Message(SQLModel, table=True):
    """Representation of a message sent from the agent -> user. Also includes function calls."""

    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    user_id: str
    agent_id: str
    role: str
    text: str
    model: str  # model used to make function call
    user: Optional[str] = None  # optional participant name
    created_at: Optional[str] = None
    function_name: Optional[str] = None  # name of function called
    function_args: Optional[str] = None  # args of function called
    function_response: Optional[str] = None  # response of function called
    embedding: List[float] = Field(default=None, sa_column=Column(Vector(1536)))

    class Config:
        arbitrary_types_allowed = True


class Document(SQLModel, table=True):
    """A document represent a document loaded into MemGPT, which is broken down into passages."""

    id: Optional[uuid.UUID] = Field(primary_key=True, default_factory=uuid.uuid4)
    user_id: str
    text: str
    data_source: str
    document_id: Optional[str] = None


class Passage(SQLModel, table=True):
    """A passage is a single unit of memory, and a standard format accross all storage backends.

    It is a string of text with an assoidciated embedding.
    """

    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    user_id: str
    text: str
    agent_id: Optional[str] = None  # set if contained in agent memory
    # TODO: don't hard code vector size
    embedding: List[float] = Field(default=None, sa_column=Column(Vector(1536)))
    data_source: Optional[str] = None  # None if created by agent
    doc_id: Optional[str] = None
    memgpt_metadata: Optional[dict] = Field(default={}, sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True
