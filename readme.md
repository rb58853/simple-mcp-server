# Simple Python MCP-Server

This repository is based on the official MCP Python SDK repository, with the objective of creating an MCP server in Python using FastMCP. The project incorporates the following basic functionalities:

- To facilitate understanding and working with the Model Context Protocol (MCP), from the fundamentals and in an accessible manner
- To provide a testing platform for MCP clients
- To integrate the server with FastAPI and offer it as a streamable HTTP service, maintaining a clear separation between the service and the client

The project focuses on the implementation of a simple MCP server that is served through FastAPI with httpstream. This approach represents the recommended methodology for creating MCP servers. To explore other implementation forms and server services, it is recommended to consult [the official documentation](https://github.com/modelcontextprotocol/python-sdk).

### What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) lets you build servers that expose data and functionality to LLM applications in a secure, standardized way. Think of it like a web API, but specifically designed for LLM interactions. MCP servers can:

- Expose data through Resources (think of these sort of like GET endpoints; they are used to load information into the LLM's context)
- Provide functionality through Tools (sort of like POST endpoints; they are used to execute code or otherwise produce a side effect)
- Define interaction patterns through Prompts (reusable templates for LLM interactions)
- And more!

## Streamable HTTP Transport

_Note: Streamable HTTP transport is superseding SSE transport for production deployments._

```python
from mcp.server.fastmcp import FastMCP

# Stateful server (maintains session state)
mcp = FastMCP("StatefulServer")

# Stateless server (no session persistence)
mcp = FastMCP("StatelessServer", stateless_http=True)

# Stateless server (no session persistence, no sse stream with supported client)
mcp = FastMCP("StatelessServer", stateless_http=True, json_response=True)

# Run server with streamable_http transport
mcp.run(transport="streamable-http")
```

### You can mount multiple FastMCP servers in a FastAPI application

```python
# echo.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="EchoServer", stateless_http=True)


@mcp.tool(description="A simple echo tool")
def echo(message: str) -> str:
    return f"Echo: {message}"
```

```python
# math.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="MathServer", stateless_http=True)


@mcp.tool(description="A simple add tool")
def add_two(n: int) -> int:
    return n + 2
```

```python
# src/fast_api/api.py
import contextlib
from fastapi import FastAPI
from mcp.echo import echo
from mcp.math import math


# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(echo.mcp.session_manager.run())
        await stack.enter_async_context(math.mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/echo", echo.mcp.streamable_http_app())
app.mount("/math", math.mcp.streamable_http_app())
```

```python
# main
from src.fast_api.api import app
```

## Run Step by Step

### 1. Requirements

To set up the project, it is necessary to install the required dependencies. Execute the following command in the terminal:

```shell
pip install -r requirements.txt
```

### 2. Run Server

Once the dependencies have been installed, the server can be launched in the terminal using the following command:

```shell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Run Client

Once the server is running correctly on the system, [the testing client](tests/client.py) can be executed as a Python file to verify functionality.
