from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus
import logging.config
import time
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

from app.api import ai_operator

import app.settings as settings

log = logging.getLogger('appLogger') 
# log.setLevel(settings.APP_DEBUG_MODE)

server = [
    # {"url": f"https://api.ags.cloudzcp.net", "description": "Staging Server"},
    # {"url": f"https://api.dev.cloudzcp.net", "description": "Dev Server"},
    # {"url": f"http://localhost:9150", "description": "Local Server"},
]

app = FastAPI(
    # root_path=f"{settings.APP_ROOT}",
    title=f"{settings.APP_TITLE}",
    description=f"{settings.APP_DESCRIPTION}",
    version=f"{settings.APP_VERSION}",
    docs_url=f"{settings.DOCS_URL}",
    openapi_url=f"{settings.OPENAPI_URL}",
    redoc_url=f"{settings.REDOC_URL}",
    default_response_class=JSONResponse,
    debug=True,
    # servers=server,
    root_path_in_servers=True
)

# app.mount(f"{settings.APP_ROOT}/html", StaticFiles(directory="public/html"), name="html")

# downgrading the openapi version to 3.0.0
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        openapi_version="3.0.0",
        servers=app.servers
    )
    app.openapi_schema = openapi_schema

    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(ai_operator.router, tags=["operator"], prefix=settings.APP_ROOT)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# from starlette_csrf import CSRFMiddleware
# import secrets
# __csrf_secret_key = secrets.token_urlsafe(16)
# log.info(f"CRSF Secret Key: {__csrf_secret_key}")
# app.add_middleware(
#     CSRFMiddleware,
#     secret=__csrf_secret_key,
#     cookie_domain="localhost",
#     cookie_name="csrftoken",
#     cookie_path="/",
#     cookie_secure=False,
#     cookie_httponly=True,
#     cookie_samesite="lax",
#     header_name="x-csrf-token",
# )

from starlette.middleware.sessions import SessionMiddleware
import secrets
__session_secret_key = secrets.token_urlsafe(32)
log.info(f"Session Secret Key: {__session_secret_key}")

app.add_middleware(
    SessionMiddleware, 
    secret_key=__session_secret_key,
    session_cookie="session_id",
    max_age=1800,
    same_site="lax",
    https_only=True,
)

@app.middleware("http")
async def http_middleware(request: Request, call_next):
    """
    HTTP Middleware to add custom headers to the response
    1. Display request information
    2. Put process time information into Header: X-Process-Time
    3. Display response information
    """
    # await __display_request_info(request)

    start_time = time.time()
 
    response = await call_next(request)
 
    process_time = (time.time() - start_time)
    response.headers["X-Process-Time"] = f'{process_time:.5f}'

    log.info(f"Process time:{process_time:.5f} - URL: {request.url} - Proceeded successfully!")
 
    # await __display_response_info(response)
    
    return response

# @app.exception_handler(AlertBackendException)
# async def exception_handler(request: Request, e: AlertBackendException):
#     return JSONResponse(
#         status_code=e.status_code,
#         content=ResponseModel(
#             result=Result.FAILED, 
#             code=e.code, 
#             message=e.detail
#         ).model_dump(exclude_none=True),
#     )

# Start the scheduler for awake the alerts snoozed time over

async def __display_request_info(request: Request):
    """
    Display request information
    """
    request_info = "\n"
    request_info += "===================== REQUEST Started ============================\n"
    request_info += f"# Headers: {dict(request.headers)}\n"

    request_info += f"# Path: {request.url.path}\n"
    request_info += f"# Method: {request.method}\n"

    body = await request.body()
    request_info += f"# Body: {body.decode()}\n"

    request_info += f"# Query Params: {dict(request.query_params)}\n"
    request_info += "===================== REQUEST Finished ===========================\n"

    log.info(request_info)

async def __display_response_info(response: StreamingResponse):
    """
    Display response information
    """
 
    response_info = "\n"
    response_info += "===================== RESPONSE Started ===========================\n"
    response_info += f"# Headers: { dict(response.headers)}\n"
    response_info += f"# Status Code: {response.status_code}\n"

    if isinstance(response, StreamingResponse):
        original_iterator = response.body_iterator

        async def __log_and_stream_response(buffer: str):
            response_body = b""
            async for chunk in original_iterator:
                response_body += chunk
                yield chunk
            buffer += f"# Body: {response_body.decode('utf-8')}\n"
            buffer += "===================== RESPONSE Finished ==========================\n"
            if (response.status_code >= HTTPStatus.BAD_REQUEST):
                log.error(buffer)
            else:
                log.info(buffer)

        response.body_iterator = __log_and_stream_response(response_info)
    else:
        response_info += f"# Body: {response}\n"
        response_info += "===================== RESPONSE Finished ==========================\n"
        log.info(response_info)


@app.get("/healthz")
async def health_check():
    return {"status": "healthy", "message": "Agent is ready"}

from chainlit.utils import mount_chainlit
mount_chainlit(app=app, target="chainlit_app.py", path="/chainlit")

log.debug(f"LangChain Agent is ready to serve!!!!!!!!!")


# from langserve import add_routes
# from app.aiops.agent import AIOpsAgent
# from app.openapi.openapi_handler import backend_api_specs
# __agent_executor = AIOpsAgent(backend_api_specs=backend_api_specs)
# add_routes(
#     app,
#     __agent_executor.get_agent_executor,
#     path="/api/agent",
#     input_type=str,  # Specify that the input should be a string
# )
# @app.get("/")
# async def root():
#     return {
#         "message": "Welcome to the LangChain Agent API",
#         "endpoints": {
#             "agent": "/api/agent/invoke",
#             "health": "/health",
#             "docs": "/docs"
#         }
#     }
