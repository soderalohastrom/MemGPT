""" This module contains the data types used by MemGPT. Each data type must include a function to create a DB model. """
import uuid
from abc import abstractmethod
from typing import Optional
import numpy as np


# Defining schema objects:
# Note: user/agent can borrow from MemGPTConfig/AgentConfig classes


class Record:
    """
    Base class for an agent's memory unit. Each memory unit is represented in the database as a single row.
    Memory units are searched over by functions defined in the memory classes
    """

    def __init__(self, user_id: str, agent_id: str, text: str, id: Optional[str] = None):
        self.user_id = user_id
        self.agent_id = agent_id
        self.text = text
        if id is None:
            self.id = uuid.uuid4()
        else:
            self.id = id
        # todo: generate unique uuid
        # todo: self.role = role (?)

    # def __repr__(self):
    #    pass


class Message(Record):
    """Representation of a message sent from the agent -> user. Also includes function calls."""

    def __init__(
        self,
        user_id: str,
        agent_id: str,
        role: str,
        text: str,
        model: str,  # model used to make function call
        user: Optional[str] = None,  # optional participant name
        created_at: Optional[str] = None,
        function_name: Optional[str] = None,  # name of function called
        function_args: Optional[str] = None,  # args of function called
        function_response: Optional[str] = None,  # response of function called
        embedding: Optional[np.ndarray] = None,
        id: Optional[str] = None,
    ):
        super().__init__(user_id, agent_id, text, id)
        self.model = model  # model name (e.g. gpt-4)
        self.created_at = created_at

        # openai info
        self.role = role  # role (agent/user/function)
        self.user = user

        # function call info (optional)
        self.function_name = function_name
        self.function_args = function_args
        self.function_response = function_response

        # embedding (optional)
        self.embedding = embedding

    # def __repr__(self):
    #    pass


class Document(Record):
    """A document represent a document loaded into MemGPT, which is broken down into passages."""

    def __init__(self, user_id: str, text: str, data_source: str, document_id: Optional[str] = None):
        super().__init__(user_id, agent_id, text, id)
        self.text = text
        self.document_id = document_id
        self.data_source = data_source
        # TODO: add optional embedding?

    def __repr__(self) -> str:
        pass


class Passage(Record):
    """A passage is a single unit of memory, and a standard format accross all storage backends.

    It is a string of text with an assoidciated embedding.
    """

    def __init__(
        self,
        user_id: str,
        text: str,
        agent_id: Optional[str] = None,  # set if contained in agent memory
        embedding: Optional[np.ndarray] = None,
        data_source: Optional[str] = None,  # None if created by agent
        doc_id: Optional[str] = None,
        id: Optional[str] = None,
        metadata: Optional[dict] = {},
    ):
        super().__init__(user_id, agent_id, text, id)
        self.text = text
        self.data_source = data_source
        self.embedding = embedding
        self.doc_id = doc_id
        self.metadata = metadata

    def __repr__(self):
        return f"Passage(text={self.text}, embedding={self.embedding})"