from contextlib import asynccontextmanager

from fastapi import FastAPI

from .mcp import mcp_app
from .oauth_routes import router
from . import tools


# Start/stop MCP with FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp_app.router.lifespan_context(mcp_app):
        yield


# Create FastAPI app
app = FastAPI(
    title="MCP Server",
    lifespan=lifespan,
)


# Add OAuth discovery routes
app.include_router(router)


# Connect MCP to FastAPI
app.mount("/", mcp_app)