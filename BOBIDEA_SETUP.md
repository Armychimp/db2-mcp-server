# bobidea Configuration

This guide explains how to configure bobidea (IntelliJ/JetBrains IDE with MCP support) to connect to the db2-mcp-server.

## Important: Use STDIO, Not HTTP

bobidea (like most MCP clients) works best with **STDIO transport**, not HTTP/SSE.

## STDIO Configuration (Recommended)

Configure bobidea to launch the MCP server as a subprocess:

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

### With Debug Logging

To troubleshoot connection issues, enable debug mode:

```json
{
  "db2-mcp-server": {
    "command": "uv",
    "args": [
      "--directory",
      "/home/armychimp/AI/db2-mcp-server",
      "run",
      "db2-mcp-server",
      "--debug"
    ],
    "env": {
      "DB2_HOST": "localhost",
      "DB2_PORT": "50000",
      "DB2_DATABASE": "TESTDB",
      "DB2_USERNAME": "db2inst1",
      "DB2_PASSWORD": "password",
      "MCP_DEBUG": "1"
    }
  }
}
```

Then check the logs in `mcp_server.log` for detailed protocol information.

## HTTP/SSE Configuration (If bobidea Supports It)

If bobidea supports connecting to an already-running HTTP/SSE server:

### Step 1: Start the server manually

```bash
export DB2_HOST=localhost
export DB2_PORT=50000
export DB2_DATABASE=TESTDB
export DB2_USERNAME=db2inst1
export DB2_PASSWORD=password

source .venv/bin/activate
db2-mcp-server --transport stream_http --debug
```

Server runs on: `http://localhost:3721/mcp/`

### Step 2: Configure bobidea

```json
{
  "db2-mcp-server-http": {
    "url": "http://localhost:3721/mcp/",
    "transport": "sse"
  }
}
```

**Important:** Use `/mcp/` with a trailing slash. The endpoint will redirect from `/mcp` to `/mcp/`.

## Troubleshooting

### 400 Bad Request Error

Enable debug logging and check `mcp_server.log`:

1. Add `--debug` flag to your config
2. Add `"MCP_DEBUG": "1"` to environment variables
3. Restart bobidea
4. Check `mcp_server.log` in the project directory

The log will show:
- Exact requests bobidea is sending
- Parameter validation errors
- Schema mismatches
- Full error stack traces

### Schema Validation Issues

The server includes explicit `"required": []` fields in the JSON schema for strict MCP clients. If bobidea reports schema issues, check:

1. Tool parameters are using correct types
2. No `Optional` types in parameters (uses empty strings/defaults instead)
3. All schema fields are explicitly defined

### Connection Timeout

- Verify DB2 is running and accessible
- Check database credentials in environment variables
- Ensure port 3721 (HTTP) is not blocked
- For STDIO mode, check bobidea can execute `uv` command

## Available Tools

Once connected, bobidea will have access to:

### list_tables
Lists tables in the DB2 database.

**Parameters:**
- `schema_name` (optional, string): Filter by schema
- `table_type` (optional, string): Filter by type ('T' for tables, 'V' for views)
- `limit` (optional, integer, default 100): Max results

**Example:** "List all tables in the MYSCHEMA schema"

## Available Prompts

### db2_query_helper
Provides guidance for DB2 query construction.

### db2_schema_analyzer
Helps analyze DB2 schema structures and relationships.

### dynamic_prompt
Loads custom prompts from JSON config (if PROMPTS_FILE is set).

## Available Resources

### db2://connection-guide
DB2 connection configuration reference.

### db2://query-templates
Common DB2 query templates and examples.

## Configuration File Location

bobidea MCP configuration is typically stored in one of these locations:

- **Linux:** `~/.config/JetBrains/<IDE>/mcp.json`
- **macOS:** `~/Library/Application Support/JetBrains/<IDE>/mcp.json`
- **Windows:** `%APPDATA%\JetBrains\<IDE>\mcp.json`

Where `<IDE>` is your specific IDE like `IntelliJIdea2024.3`, `PyCharm2024.3`, etc.

Check bobidea documentation for the exact path in your version.

## Verification

After configuration:

1. Restart bobidea
2. Check the MCP status/connection indicator
3. Try: "List all tables in the database"
4. Check `mcp_server.log` for connection logs

## Need Help?

- See [DEBUG_MODE.md](DEBUG_MODE.md) for comprehensive debugging
- See [README.md](README.md) for general setup
- Check [HTTP_MODE_USAGE.md](HTTP_MODE_USAGE.md) for HTTP/SSE details
- Report issues: https://github.com/Armychimp/db2-mcp-server/issues
