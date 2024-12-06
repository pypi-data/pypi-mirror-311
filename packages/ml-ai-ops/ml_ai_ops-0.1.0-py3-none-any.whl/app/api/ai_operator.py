from langchain.tools import StructuredTool
from datetime import datetime
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.aiops.agent import AIOpsAgent
from app.openapi.openapi_handler import backend_api_specs

from app.aiops import aiops_agent
from app.aiops import header_manager


log = logging.getLogger('appLogger') 

router = APIRouter()

@router.get(
    "/tools", 
    summary="Get tools of the agent", 
    response_class=JSONResponse,
    response_model=List[Dict[str, str]],
    response_model_by_alias=False,
    response_model_exclude_none=False)
async def get_tools(
) -> List[Dict[str, str]]:
    """ A restful API to get tools of the agent

    Returns
    -------
    List[StructuredTool]
    """
    return aiops_agent.get_tools

@router.post(
    "/tools", 
    summary="Extends tools of the agent", 
    response_class=JSONResponse,
    response_model=Dict[str, Any],
    response_model_by_alias=False,
    response_model_exclude_none=False)
async def get_tools(
    tool_openapi_path: str = Query(..., title="OpenAPI Path", description="OpenAPI Path to the tool")
) -> Dict[str, Any]:
    """ A restful API to get tools of the agent

    Returns
    -------
    List[StructuredTool]
    """
    return aiops_agent.get_tools

@router.post(
    "/set_cookies", 
    summary="Run the agent with the given input",
    response_class=JSONResponse,
    response_model=Dict[str, Any],
    response_model_by_alias=False,
    response_model_exclude_none=True)
async def run(
    request: Request,
    cookies: str = Query(..., title="Cookies", description="Cookies to the agent"),
) -> Dict[str, Any]:
    """ A restful API to run the agent with the given input

    Parameters
    ----------
    cookies : str

    Returns
    -------
    Dict[str, Any]
    """
    # header = request.headers
    # cookies = request.cookies
    header_manager.set_cookies(cookies)

    return {"result": "success"}
