<div align="center">
  <h1>MCP Memory</h1>
  <p><strong>Memory Implementation in MCP and python</strong></p>
  <p>
    <img src="https://img.shields.io/badge/python->=3.11-blue">
    <a href="https://pypi.org/project/mcp-memory/">
      <img src="https://img.shields.io/pypi/v/mcp-memory.svg">
    </a>
  </p>
</div>



🤔 [MCP](https://github.com/modelcontextprotocol) stands for Model Context Protocol, meaning a open protocol between Agent and Others

🧠 Memory is a great tool/storage for your AI, so that AI can remember user and stuff.

✅ The repo implements a memory mechanism and a MCP server



## Quick Start

Add this to your `claude_desktop_config.json`

```json
{
  "mcpServers": {
    "memory": {
      "command": "uvx",
      "args": ["mcp-memory"]
    }
  }
}
```

Or use it in Python:

```shell
uv install mcp-memory
# or
pip install mcp-memory
```



## Features

TODO



## Resources

- A Memory MCP server in TS. [link](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)
- LangGraph concepts. [link](https://langchain-ai.github.io/langgraph/concepts/memory/)