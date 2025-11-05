# Debug Mode

The MCP server includes comprehensive debug logging to help diagnose connection and protocol issues.

## Enabling Debug Mode

### Option 1: Command Line Flag

```bash
source .venv/bin/activate

# For STDIO mode
db2-mcp-server --debug

# For HTTP mode
db2-mcp-server --transport stream_http --debug
```

### Option 2: Environment Variable

```bash
export MCP_DEBUG=1  # or "true" or "yes"

# Then run normally
db2-mcp-server
```

### Option 3: Claude Code Configuration

Add the `MCP_DEBUG` environment variable to your `.claude/mcp.json`:

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

## What Gets Logged

When debug mode is enabled, the following information is logged to `mcp_server.log`:

### Startup Information
- Transport type (stdio/http)
- Database connection settings
- Port configuration (for HTTP mode)
- MCP middleware initialization

### MCP Protocol Calls
- `list_tools` - Lists available tools
- `call_tool` - Tool invocations with arguments
- `list_prompts` - Prompt listing
- `get_prompt` - Prompt retrieval
- `list_resources` - Resource listing
- `read_resource` - Resource reading

For each call, logs include:
- Function name
- Arguments (full detail)
- Context information
- Return values
- Exception traces (if errors occur)

### Tool Execution
- Tool name and arguments
- Database queries being executed
- Number of results returned
- Errors and stack traces

## Log File Location

Logs are written to: **`mcp_server.log`** in the current directory

The log file:
- Maximum size: 4MB
- Rotation: Overwrites when full (no backups)
- Format: `timestamp - module - level:line - message`

## Example Debug Output

```
2025-11-05 12:00:00 - db2_mcp_server.core - INFO:52 - Starting DB2 MCP Server
2025-11-05 12:00:00 - db2_mcp_server.core - INFO:53 - Transport: stdio
2025-11-05 12:00:00 - db2_mcp_server.core - INFO:54 - DB2_HOST: localhost
2025-11-05 12:00:00 - db2_mcp_server.core - INFO:55 - DB2_PORT: 50000
2025-11-05 12:00:00 - db2_mcp_server.core - INFO:56 - DB2_DATABASE: TESTDB
2025-11-05 12:00:00 - db2_mcp_server.core - DEBUG:51 - Debug logging enabled
2025-11-05 12:00:00 - db2_mcp_server.core - DEBUG:56 - Debug middleware enabled
2025-11-05 12:00:00 - db2_mcp_server.debug_middleware - DEBUG:60 - Wrapped MCP method: list_tools
2025-11-05 12:00:00 - db2_mcp_server.debug_middleware - DEBUG:60 - Wrapped MCP method: call_tool
2025-11-05 12:00:01 - db2_mcp_server.debug_middleware - DEBUG:12 - === MCP Call: list_tools ===
2025-11-05 12:00:01 - db2_mcp_server.debug_middleware - DEBUG:13 - Args: ()
2025-11-05 12:00:01 - db2_mcp_server.debug_middleware - DEBUG:14 - Kwargs: {}
2025-11-05 12:00:01 - db2_mcp_server.tools.list_tables - DEBUG:126 - list_tables called with args: ListTablesInput(schema_name='', table_type='', limit=100)
2025-11-05 12:00:01 - db2_mcp_server.tools.list_tables - DEBUG:132 - list_tables returning 169 tables
```

## Troubleshooting bobidea Connection

If bobidea shows a **400 Bad Request** error, enable debug mode and check:

1. **Startup logs** - Verify all settings are correct
2. **MCP Protocol logs** - See what requests bobidea is sending
3. **Tool execution logs** - Check if tool calls are reaching the server
4. **Error traces** - Look for exceptions or validation errors

Common issues:
- Missing or invalid JSON schema fields
- Incorrect parameter types
- Protocol version mismatch
- Authentication/credential issues

## Disabling Debug Mode

Simply remove the `--debug` flag or unset the `MCP_DEBUG` environment variable:

```bash
unset MCP_DEBUG
db2-mcp-server
```

Or update your configuration to remove the debug settings.

## Log Level Control

You can also control the base log level independently:

```bash
export LOG_LEVEL=DEBUG   # DEBUG, INFO, WARNING, ERROR, CRITICAL
db2-mcp-server
```

Note: `MCP_DEBUG=1` automatically sets `LOG_LEVEL=DEBUG` plus enables additional middleware logging.
