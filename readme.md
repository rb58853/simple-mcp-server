# Simple Python MCP-Server

<div align = center>

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Last commit](https://img.shields.io/github/last-commit/rb58853/simple-mcp-server.svg?style=flat)](https://github.com/rb58853/simple-mcp-server/commits)
[![Commit activity](https://img.shields.io/github/commit-activity/m/rb58853/simple-mcp-server)](https://github.com/rb58853/simple-mcp-server/commits)
[![Stars](https://img.shields.io/github/stars/rb58853/simple-mcp-server?style=flat&logo=github)](https://github.com/rb58853/simple-mcp-server/stargazers)
[![Forks](https://img.shields.io/github/forks/rb58853/simple-mcp-server?style=flat&logo=github)](https://github.com/rb58853/simple-mcp-server/network/members)
[![Watchers](https://img.shields.io/github/watchers/rb58853/simple-mcp-server?style=flat&logo=github)](https://github.com/rb58853/simple-mcp-server)
[![Contributors](https://img.shields.io/github/contributors/rb58853/simple-mcp-server)](https://github.com/rb58853/simple-mcp-server/graphs/contributors)

</div>

A python implementation of the **Model Context Protocol (MCP)** server with `fastmcp` and `fastapi`.

## Table of Contents

* [Overview](#overview)
* [Streamable HTTP Transport](#streamable-http-transport)
* [Deployment](#deployment)
* [Deployment](#deployment)
* [License](#license)

## Overview

This repository is based on the official MCP Python SDK repository, with the objective of creating an MCP server in Python using FastMCP. The project incorporates the following basic functionalities:

* To facilitate understanding and working with the Model Context Protocol (MCP), from the fundamentals and in an accessible manner
* To provide a testing platform for MCP clients
* To integrate the server with FastAPI and offer it as a streamable HTTP service, maintaining a clear separation between the service and the client

The project focuses on the implementation of a simple MCP server that is served through FastAPI with httpstream. This approach represents the recommended methodology for creating MCP servers. To explore other implementation forms and server services, it is recommended to consult [the official documentation](https://github.com/modelcontextprotocol/python-sdk).

## Transport

### Streamable HTTP Transport

>Note: Streamable HTTP transport is superseding SSE transport for production deployments.

```python
from mcp.server.fastmcp import FastMCP
# Stateless server (no session persistence)
mcp = FastMCP("StatelessServer", stateless_http=True)
```

You can mount multiple FastMCP servers in a FastAPI application

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
# fast_api.py
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

## Deployment

### Local Deployment

To set up the development environment, execute the following commands:

**1. Install project dependencies**

   ```bash
   pip install -r requirements.txt
   ```

**2. Start the server in development mode**

   ```bash
   uvicorn src.run:app --host 0.0.0.0 --port 8000 --reload
   ```

**3. Run tests**

   ```bash
   python tests/run.py
   ```

## Docker Deployment

The project can be run using Docker Compose:

```bash
docker compose -f docker-compose.yml up -d --force-recreate
```

## Use Case

Para probar el uso correcto de este servidor puedes instalar el paquete `mcp-llm-client` siguiendo los siguientes pasos:

```shell
pip install mcp-llm-client
```

## License

MIT License. See [`license`](license).
