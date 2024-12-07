from abc import ABC, abstractmethod
from collections import deque
from typing import Union, List, Optional, Type

from duowen_agent.llm.chat_model import OpenAIChat
from duowen_agent.llm.embedding_model import OpenAIEmbedding, EmbeddingCache
from duowen_agent.llm.entity import MessagesSet
from duowen_agent.llm.rerank_model import GeneralRerank
from duowen_agent.rag.retrieval.retrieval import Retrieval
from duowen_agent.tools.base import Tool
from duowen_agent.utils.string_template import StringTemplate
from pydantic import BaseModel


class BaseAgent(ABC):

    def __init__(self, llm: OpenAIChat = None, retrieval_instance: Retrieval = None,
                 embedding_instance: Union[EmbeddingCache, OpenAIEmbedding] = None, rerank_model: GeneralRerank = None,
                 callback: deque = None, tools: Optional[List[Tool]] = None, agents: Optional[List['BaseAgent']] = None,
                 output_schema: Optional[Union[Type[BaseModel], StringTemplate, dict, str]] = None, **kwargs):
        self.llm = llm
        self.retrieval_instance = retrieval_instance
        self.embedding_instance = embedding_instance
        self.rerank_model = rerank_model
        self.callback = callback
        self.tools = tools
        self.agents = agents
        self.output_schema = output_schema
        self.kwargs = kwargs

    def put_callback(self, item):
        if self.callback:
            self.callback.append(item)

    @abstractmethod
    def chat(self, user_input: Union[MessagesSet, str], **kwargs):
        ...
