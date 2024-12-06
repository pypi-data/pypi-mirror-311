from langchain.tools import StructuredTool
from langchain_openai import ChatOpenAI
from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.schema.runnable import Runnable

from app.aiops.prompt import get_aiops_prompt_template
from app.util.tool_generator import create_structured_tools_from_openapi

import app.settings as settings

class AIOpsAgent:
    def __init__(
        self,
        *,
        backend_api_specs: List[str],
        model_name: str = "gpt-4o-mini"
    ):
        self.__tools: List[StructuredTool] = []

        for api_path in backend_api_specs:
            self.__tools.extend(create_structured_tools_from_openapi(api_path))

        self.__api_key = settings.OPENAI_API_KEY
        if self.__api_key is None:
            raise ValueError('OPENAI_API_KEY is not set')
        
        self.__llm = ChatOpenAI(api_key=self.__api_key, temperature=0, model_name=model_name)

        self.__prompt = ChatPromptTemplate.from_template(get_aiops_prompt_template())

        self.__agent: Runnable = None

        self.__agent_executor: AgentExecutor = None

    @property
    def get_agent(self) -> Runnable:
        return self.__agent

    @property
    def get_tools(self) -> List[Dict[str, str]]:
        tools = []
        for tool in self.__tools:
            tools.append({
                'name': tool.name,
                # 'description': tool.description,
                })
        return tools
    
    def extend_tools(self, tools: List[StructuredTool]):
        self.__tools.extend(tools)
        self.__reset_agent_executor()
    
    @property
    def get_agent_executor(self) -> AgentExecutor:
        if self.__agent_executor is None:
            self.__reset_agent_executor()

        return self.__agent_executor
    
    def __reset_agent_executor(self):
        self.__agent = create_structured_chat_agent(
            llm=self.__llm,
            tools=self.__tools,
            prompt=self.__prompt
        )

        self.__agent_executor = AgentExecutor(
            agent=self.__agent,
            tools=self.__tools,
            verbose=True,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )

from app.openapi.openapi_handler import backend_api_specs
aiops_agent = AIOpsAgent(backend_api_specs=backend_api_specs)

from app.util.header_manager import HeaderManager
header_manager = HeaderManager()
