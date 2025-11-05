# Using HTTP/SSE Mode

The MCP server supports HTTP with Server-Sent Events (SSE) transport, but **most IDEs only support STDIO**.

## What Works

### ✓ STDIO Mode (Claude Code, Claude Desktop, bobide)

```bash
# This is what Claude Code uses automatically
uv --directory /path/to/db2-mcp-server run db2-mcp-server
```

Configuration in `.claude/mcp.json`:
```json
{
  "db2-mcp-server": {
    "command": "uv",
    "args": [
      "--directory",
      "/home/armychimp/AI/db2-mcp-server",
      "run",
      "db2-mcp-server"
    ],
    "env": {
      "DB2_HOST": "localhost",
      "DB2_PORT": "50000",
      "DB2_DATABASE": "TESTDB",
      "DB2_USERNAME": "db2inst1",
      "DB2_PASSWORD": "password"
    }
  }
}
```

## HTTP/SSE Mode (For Testing Only)

### Starting the Server

```bash
# Option 1: Use the helper script
./test_mcp_http.sh

# Option 2: Manual start
export DB2_HOST=localhost
export DB2_PORT=50000
export DB2_DATABASE=TESTDB
export DB2_USERNAME=db2inst1
export DB2_PASSWORD=password
export MCP_PORT=3721  # Optional, defaults to 3721

source .venv/bin/activate
db2-mcp-server-stream-http
```

The server will run on: **http://0.0.0.0:3721/mcp**

### Testing with MCP Inspector

Once the server is running, you can connect with MCP Inspector:

```bash
# In another terminal
npx @modelcontextprotocol/inspector \
  --transport sse \
  --server-url http://localhost:3721/mcp
```

This will open a web UI at http://localhost:5173 to test the MCP server.

### Why Not Use HTTP with IDEs?

**Claude Code and Claude Desktop only support STDIO transport**, not HTTP/SSE. They:
1. Launch the MCP server as a subprocess
2. Communicate via stdin/stdout using JSON-RPC
3. Cannot connect to already-running HTTP servers

HTTP/SSE mode is useful for:
- Testing with MCP Inspector
- Building custom web-based MCP clients
- Debugging MCP protocol communication
- Running a persistent MCP service

But for day-to-day IDE usage, stick with STDIO transport.

## Port Configuration

The HTTP server port can be configured via environment variable:

```bash
export MCP_PORT=8080
db2-mcp-server-stream-http
# Server runs on http://0.0.0.0:8080/mcp
```

Default port: **3721**
