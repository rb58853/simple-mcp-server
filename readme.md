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
* [Authorization](#oauth)
* [Deployment](#deployment)
* [Use Case](#use-case)
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

## Autorization (OAuth)

For the authorization system, a package offering a simple client-credentials authorization method is used, called [`mcp-oauth`](https://github.com/rb58853/mcp-oauth). This package allows running an OAuth server in parallel with the MCP server. The source code can be found in [oauth_server.py](src/services/fast_mcp/private_server/oauth_server.py).

```python
# oauth_server.py
from mcp_oauth import (
    OAuthServer,
    SimpleAuthSettings,
    AuthServerSettings,
)

from dotenv import load_dotenv

load_dotenv()

OAUTH_HOST = "127.0.0.1"
OAUTH_PORT = 9000
OAUTH_SERVER_URL = f"http://{OAUTH_HOST}:{OAUTH_PORT}"


def run_oauth_server():
    server_settings: AuthServerSettings = AuthServerSettings(
        host=OAUTH_HOST,
        port=OAUTH_PORT,
        server_url=f"{OAUTH_SERVER_URL}",
        auth_callback_path=f"{OAUTH_SERVER_URL}/login",
    )
    auth_settings: SimpleAuthSettings = SimpleAuthSettings(
        superusername=os.getenv("SUPERUSERNAME"),
        superuserpassword=os.getenv("SUPERUSERPASSWORD"),
        mcp_scope="user",
    )
    oauth_server: OAuthServer = OAuthServer(
        server_settings=server_settings, auth_settings=auth_settings
    )
    oauth_server.run_starlette_server()


if __name__ == "__main__":
    run_oauth_server()

```

To start this server, you can open a terminal in the root directory of the project and execute:

```shell
python3 src/services/fast_mcp/private_server/oauth_server.py
```

### MCP Integration

Once the OAuth server is running, it must be integrated with the MCP server by providing the address where the OAuth server is running to the MCP server:

```python
def create_private_server(settings: ServerSettings = ServerSettings()) -> FastMCP:

    token_verifier = IntrospectionTokenVerifier(
        introspection_endpoint=settings.auth_server_introspection_endpoint,
        server_url=str(settings.server_url),
        validate_resource=settings.oauth_strict,  # Only validate when --oauth-strict is set
    )

    mcp: FastMCP = FastMCP(
        name="private-example-server",
        instructions="This server specializes in private operations of user profiles data",
        debug=True,
        # Auth configuration for RS mode
        token_verifier=token_verifier,
        auth=AuthSettings(
            issuer_url=settings.auth_server_url,
            required_scopes=[settings.mcp_scope],
            resource_server_url=settings.server_url,
        ),
    )

```

The MCP requires a `TokenVerifier`, for which a simple one provided by the `mcp_oauth` package is used. In this case, `settings.auth_server_url` must be the address where the OAuth server is running, for example `"http://127.0.0.1:9000"`. For further configuration details, please refer to the code in [`private_server/server.py`](/src/services/fast_mcp/private_server/server.py).

### Configuration

This OAuth server uses a credential-based system for authentication (initial authorization token acquisition). You must fill the `.env` file with the following variables:

```env
SUPERUSERNAME=user
SUPERUSERPASSWORD=password
```

## Deployment

### Local Deployment

To set up the development environment, execute the following commands:

**1. Install project dependencies**

   ```bash
   pip install -r requirements.txt
   ```

**2.1 Start the server in development mode**

   ```bash
   uvicorn src.app:app --host 127.0.0.1 --port 8000 --reload
   ```

**2.2 Start the oauth server**

```bash
python3 src/services/fast_mcp/private_server/oauth_server.py
```

**3. Verify Proper Server Startup**

To confirm that the server is operating correctly, open a web browser and navigate to the address [http://127.0.0.1:8000](http://127.0.0.1:8000). This should redirect to a user help page that provides guidance on how to use the server.

**4. Run tests**

   ```bash
   python tests/run.py
   ```

### Docker Deployment

The project can be run using Docker Compose:

```bash
docker compose -f docker-compose.yml up -d --build
```

## Use Case

To verify the correct operation of this server, it is recommended to install the [`mcp-llm-client`](https://github.com/rb58853/python-mcp-client) package and create a project based on it by following the steps outlined below:
> ⚠️ **Configuration Note:** To use this chat with an LLM, an OpenAI API key is required. If you do not have one, you can create it by following the instructions on the [official OpenAI page](https://platform.openai.com/login).

**1. Server Deployment**

Deploy this server according to the instructions provided in the [Deployment](#deployment) section. This step is essential, as the server must be running either locally or on a cloud server. Once the server is deployed, it can be used through the MCP client.

<!-- **2. Install the package**

```shell
pip install mcp-llm-client
``` -->

**2. Clone a template from GitHub**

Clone a template from GitHub that provides a simple base to use the MCP client:

```shell
# clone repo
git clone https://github.com/rb58853/template_mcp_llm_client.git

# change to project dir
cd template_mcp_llm_client

# install dependencies
pip install -r requirements.txt
```

**3. Add Server to Configuration**

In the cloned project, locate the `config.json` file in the root directory and add the following configuration inside the **mcp_servers** object:

```json
{
    "mcp_servers": {
        "example_public_server": {
            "transport": "httpstream",
            "httpstream-url": "http://127.0.0.1:8000/public-example-server/mcp",
            "name": "example-public-server",
            "description": "Example public server."
        },
        "example_private_mcp": {
            "transport": "httpstream",
            "httpstream-url": "http://127.0.0.1:8000/private-example-server/mcp",
            "name": "example-private-server",
            "description": "Example private server with oauth required.",
            "auth": {
                "required": true,
                "server": "http://127.0.0.1:9000",
                "secrets": {
                    "username": "user",
                    "password": "password"
                }
            }
        }
    }
}
```

> 💡 **Hint:** Once the server is deployed, you can access its root URL to obtain help. This section provides the exact configuration needed to add the server to the MCP client. For example, opening `http://127.0.0.1:8000` in a browser will redirect to the help page.

**4. Execution**

Follow the instructions in the `readme.md` file of the cloned project to run a local chat using this MCP server. Typically, this is done by running the following command in the console:

```shell
# Run app (after set OPENAI-API-KEY and add servers to config)
python3 main.py
```

### Bibliography

For more detailed information on using this MCP client, please refer to [its official repository](https://github.com/rb58853/python-mcp-client).

## License

MIT License. See [`license`](license).
