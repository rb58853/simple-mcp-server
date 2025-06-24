"""html doc for expose in host"""

from ..environment import EnvAPI

end: str = """
</html>
"""

base: str = """<html>

<head>
    <style>
        :root {
            --bg-primary: #282c34;
            --text-primary: #abb2bf;
            --heading-color: #61afef;
            --accent-color: #98c379;
            --border-color: #404452;
            --shadow-color: rgba(0, 0, 0, 0.3);
        }

        /* Estilos base del cuerpo */
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;

            /* Modificaciones para modo oscuro */
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }

        /* Estilos de encabezados */
        h1 {
            color: var(--heading-color);
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 10px;
        }

        h2 {
            color: #89ddff;
            /* Azul más claro que h1 */
            padding-bottom: 8px;
            margin: 1.2em 0 0.8em;
            font-size: 1.5em;
        }

        h3 {
            color: #c792ea;
            /* Tonalidad morada suave */
            padding-bottom: 4px;
            margin: 1em 0 0.5em;
            font-size: 1.25em;
        }

        /* Estilos adicionales para mejor legibilidad */
        p {
            margin: 1em 0;
            opacity: 0.95;
        }

        pre {
            background-color: rgba(98, 151, 219, 0.1);
            border-radius: 8px;
            padding: 1em;
            overflow-x: auto;
        }

        li code {
            background-color: rgba(255, 30, 127, 0.1);
            /* Rosa muy suave con opacidad */
            color: rgb(255, 0, 111);
            /* Rosa muy suave con opacidad */
            padding: 0px;
            padding-inline: 5px;
            border-radius: 3px;
        }
        
        .inline-code {
            background-color: rgba(255, 30, 127, 0.1);
            /* Rosa muy suave con opacidad */
            color: rgb(255, 0, 111);
            /* Rosa muy suave con opacidad */
            padding: 0px;
            padding-inline: 5px;
            border-radius: 3px;
        }
        
        .horizontal-ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .horizontal-ul li {
            display: inline-block;
            padding: 0 10px;
        }

        /* Estilo principal del código */
        code {
            font-family: 'Consolas', Monaco, 'Andale Mono', monospace;
            line-height: 1.5;
        }

        /* Estilos para los elementos destacados */
        span {
            background-color: transparent;
        }

        .lang-python {
            color: #abb2bf;
        }

        /* Palabras clave */
        .hljs-keyword {
            color: #c678dd;
        }

        /* Funciones */
        .hljs-function .hljs-title {
            color: #61afef;
        }

        /* Importaciones */
        .hljs-import {
            color: #98c379;
        }

        /* Comentarios */
        .hljs-comment {
            color: #5c6370;
            font-style: italic;
        }

        /* Strings */
        .hljs-string {
            color: #98c379;
        }

        /* Números */
        .hljs-number {
            color: #d19a66;
        }

        /* Operadores */
        .hljs-operator {
            color: #56b6c2;
        }

        /* Clases */
        .hljs-class {
            color: #e06c75;
        }

        /* Métodos */
        .hljs-method {
            color: #61afef;
        }
    </style>
</head>

<body>
    <h1 id="mcp-server-for-supabase">Example MCP Server</h1>
    <p>This MCP server implements the Model Context Protocol (MCP) through HTTPstream. The server is designed to expose specific tools and resources that allow client
        applications.</p>
    <h2 id="main-features">Main Features</h2>
    <ul>
        <li>Exposure of services through HTTPstream</li>
        <li>Secure connection management</li>
        <li>Interface compatible with the MCP protocol</li>
    </ul>
    <h2 id="client-configuration">Client Configuration</h2>
    <p>To connect to the server, use the following Python example codes:</p>
    <h3 id="client-for-server-without-authorization">Client for server without authorization</h3>
    <pre><code class="lang-python"><span class="hljs-keyword">from</span> mcp.client.streamable_http <span class="hljs-keyword">import</span> streamablehttp_client
<span class="hljs-keyword">from</span> mcp <span class="hljs-keyword">import</span> ClientSession
<span class="hljs-keyword">async</span> <span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">main</span><span class="hljs-params">()</span>:</span>
    <span class="hljs-comment"># Connect to HTTPstream server</span>
    <span class="hljs-keyword">async</span> <span class="hljs-keyword">with</span> streamablehttp_client(<span class="hljs-string">"http://0.0.0.0:8080/{server_name}/mcp"</span>) <span class="hljs-keyword">as</span> (
            read_stream,
            write_stream,
            _,
    ):
        <span class="hljs-comment"># Create session using client streams</span>
        <span class="hljs-keyword">async</span> <span class="hljs-keyword">with</span> ClientSession(read_stream, write_stream) <span class="hljs-keyword">as</span> session:
            <span class="hljs-comment"># Initialize connection</span>
            <span class="hljs-keyword">await</span> session.initialize()
            <span class="hljs-comment"># List available tools</span>
            tools = <span class="hljs-keyword">await</span> session.list_tools()
            <span class="hljs-comment"># List available resources</span>
            resources = <span class="hljs-keyword">await</span> session.list_resource_templates()
            <span class="hljs-comment"># List available prompts</span>
            prompts = <span class="hljs-keyword">await</span> session.list_prompts()

<span class="hljs-keyword">if</span> __name__ == <span class="hljs-string">"__main__"</span>:
    <span class="hljs-keyword">import</span> asyncio
    asyncio.run(main())
</code></pre>

    <h1 id="services">Services</h1>
    <h2 id="tools">Tools</h2>
    <ul>
        <li><code>set_user_profile:</code> Set the user profile information in database for user_id.</li>
    </ul>
    <h2 id="resoruces">Resoruces</h2>
    <ul>
        <li><code>get_user_profile:</code> Gets the user profile information for user_id.</li>
    </ul>
    <h2 id="prompts">Prompts</h2>
    <ul>
        <li><code>prompt:</code> action.</li>
    </ul>
    
</body>
"""


def server_info(
    name: str,
    description: str,
    tools: list[str],
    is_auth: bool = False,
) -> str:
    http_path = f"{EnvAPI.DNS if EnvAPI.DNS else EnvAPI.BASE_IP}/{name}/mcp"
    text: str = f"""
    <body>
    <h2>MCP server {name}</h2>
    <p>{description}</p>
    <b>http path:</b><code class = "inline-code">{http_path}</code>
    <h3>Aviable Tools</h3>
    <ul class = "horizontal-ul">
    """
    for tool in tools:
        text += f"<li><code>{tool}</code></li>"
    text += "</ul>"

    text += (
        f""" <h3>Server Config</h3>
    You can use <a href="https://github.com/rb58853/python-mcp-client">mcp-llm-client</a> and paste this configuration
    <pre><code class="lang-python">
    <span class="hljs-string">"{name}"</span>: """
        + "{"
        + f"""
        <span class="hljs-string">"http"</span>: <span class="hljs-string">"{http_path}"</span>,
        <span class="hljs-string">"name"</span>: <span class="hljs-string">"{name}"</span>,
        <span class="hljs-string">"description"</span>: <span class="hljs-string">"{description}"</span>
    """
        + """}
    </code></pre>"""
    )
    return text + "</body>"
