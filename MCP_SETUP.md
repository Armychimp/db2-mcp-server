# MCP Server Setup Guide

## Overview
This DB2 MCP Server is now installed and ready to use. It provides tools for interacting with IBM DB2 databases through the Model Context Protocol (MCP).

## Configuration Complete ✓

### 1. Dependencies Installed
All Python dependencies have been installed using `uv` in a virtual environment at `.venv/`.

### 2. Environment Variables
A `.env` file has been created with the following variables:
- `DB2_HOST` - Your DB2 server hostname
- `DB2_PORT` - DB2 port (default: 50000)
- `DB2_DATABASE` - Database name
- `DB2_USERNAME` - Read-only database user
- `DB2_PASSWORD` - Database password

**⚠️ IMPORTANT**: Edit the `.env` file with your actual DB2 credentials before using the server.

### 3. Code Fixed
Updated `src/db2_mcp_server/tools/list_tables.py` to read connection details from environment variables instead of hardcoded values.

## Using the MCP Server

### Option 1: With Claude Desktop

Add this configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "db2-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/home/armychimp/AI/db2-mcp-server",
        "run",
        "db2-mcp-server"
      ],
      "env": {
        "DB2_HOST": "your_db2_host",
        "DB2_PORT": "50000",
        "DB2_DATABASE": "your_database",
        "DB2_USERNAME": "your_username",
        "DB2_PASSWORD": "your_password"
      }
    }
  }
}
```

### Option 2: Direct CLI Usage

#### STDIO Mode (for MCP clients):
```bash
source .venv/bin/activate
python -m db2_mcp_server.core --transport stdio
```

#### HTTP Mode (for testing):
```bash
source .venv/bin/activate
python -m db2_mcp_server.core --transport stream_http
# Server will run on http://127.0.0.1:3721/mcp
```

Or use the convenience command:
```bash
source .venv/bin/activate
db2-mcp-server-stream-http
```

## Available Tools

Once connected, the MCP server provides these tools:

1. **list_tables** - List all tables in the DB2 database
   - Optional parameters: schema, table_type, limit

2. **Resources**:
   - `db2://connection-guide` - DB2 connection configuration guide
   - `db2://query-templates` - Common DB2 query templates

## Testing the Connection

After configuring your DB2 credentials in `.env`, you can test the connection:

```bash
source .venv/bin/activate
python -c "from dotenv import load_dotenv; load_dotenv(); from src.db2_mcp_server.tools.list_tables import list_tables_logic, ListTablesInput; print(list_tables_logic(ListTablesInput()))"
```

## Troubleshooting

### Connection Issues
- Verify DB2 server is accessible from your machine
- Check firewall rules for port 50000 (or your configured port)
- Ensure DB2 credentials are correct
- Test connection using `db2` CLI tools first

### Import Errors
- Make sure you're using the virtual environment: `source .venv/bin/activate`
- Reinstall dependencies: `uv sync`

### Permission Issues
- Ensure the database user has SELECT permissions on system catalogs
- User should have read-only access (no INSERT/UPDATE/DELETE)

## Security Notes

- This server is designed to be read-only
- Always use a database user with minimal permissions (SELECT only)
- Never commit the `.env` file to version control
- Use `.env.example` as a template for sharing configuration format

## Running Tests

```bash
source .venv/bin/activate
pytest --cov=src/db2_mcp_server --cov-report=html tests/
```

Current test coverage: **92.98%**

## Next Steps

1. Edit `.env` with your actual DB2 credentials
2. Test the connection using the test command above
3. Configure Claude Desktop or your MCP client to use this server
4. Start querying your DB2 database through Claude!
