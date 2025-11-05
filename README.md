# db2-mcp-server

[![PyPI version](https://badge.fury.io/py/db2-mcp-server.svg)](https://badge.fury.io/py/db2-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen.svg)](https://github.com/Armychimp/db2-mcp-server)

## Overview
The `db2-mcp-server` is a Python-based Model Context Protocol (MCP) server for interacting with IBM DB2 databases. It enables AI assistants like Claude to query DB2 databases through a secure, read-only interface.

## Features
- **List Tables Tool**: Query tables from your DB2 database with filtering by schema and table type
- **Built-in Prompts**: Pre-configured prompts for DB2 query help and schema analysis
- **Dynamic Prompt Loading**: Load custom prompts from JSON configuration files for flexible query assistance
- **Resource Templates**: Access DB2 connection guides and query templates
- **Read-Only Access**: Security-focused design prevents write operations
- **Environment-Based Configuration**: Secure credential management through environment variables

## Requirements
- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) (package manager)
- IBM DB2 database (local or remote)
- Optional: Docker for local DB2 instance

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Armychimp/db2-mcp-server.git
cd db2-mcp-server
```

### 2. Install Dependencies

#### Option A: Using uv (Recommended)
```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync
```

#### Option B: Using pip
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Optional: Install development dependencies
pip install -r requirements-dev.txt
```

### 3. Set Up DB2 Database

#### Option A: Use Docker (Recommended for Development)
```bash
# Start a DB2 container
docker run -d \
  --name db2 \
  --privileged=true \
  -p 50000:50000 \
  -e LICENSE=accept \
  -e DB2INST1_PASSWORD=password \
  -e DBNAME=SAMPLE \
  icr.io/db2_community/db2
```

**Copy-paste one-liner:**
```bash
docker run -d --name db2 --privileged=true -p 50000:50000 -e LICENSE=accept -e DB2INST1_PASSWORD=password -e DBNAME=SAMPLE icr.io/db2_community/db2
```

```bash
# Wait 3-5 minutes for DB2 to initialize
# Check if ready:
docker logs db2 2>&1 | grep -i "setup has completed"
```

#### Option B: Use Existing DB2 Instance
Ensure you have:
- DB2 hostname and port
- Database name
- Read-only user credentials

### 4. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your DB2 connection details
nano .env
```

Example `.env` configuration for Docker:
```bash
DB2_HOST=localhost
DB2_PORT=50000
DB2_DATABASE=TESTDB       # Use the actual DB name from step 5
DB2_USERNAME=db2inst1
DB2_PASSWORD=password
```

### 5. Verify Database Name

The Docker container creates a database, but the name might not be what you expect. Check it:

```bash
docker exec db2 bash -c "su - db2inst1 -c 'db2 list database directory'"
```

Update your `.env` file with the actual database name (often `TESTDB` instead of `SAMPLE`).

### 6. Create Test Data (Optional)

Populate the database with sample tables:

```bash
source .venv/bin/activate
python setup_test_data.py
```

This creates:
- **CUSTOMERS** table (5 rows)
- **PRODUCTS** table (7 rows)
- **EMPLOYEES** table (6 rows)
- **ORDERS** table (8 rows)

View the test data:
```bash
python view_test_data.py
```

### 7. Test the Connection
```bash
source .venv/bin/activate
python -c "
from dotenv import load_dotenv
load_dotenv()
from src.db2_mcp_server.tools.list_tables import list_tables_logic, ListTablesInput
result = list_tables_logic(ListTablesInput())
print(f'✓ Connected! Found {result.count} tables')
"
```

## Using with Claude Code

The easiest way to use this MCP server with Claude Code is via the CLI:

```bash
# Navigate to the project directory
cd /path/to/db2-mcp-server

# Add the MCP server (replace /path/to/db2-mcp-server with your actual path)
claude mcp add --transport stdio db2-mcp-server \
  --env DB2_HOST=localhost \
  --env DB2_PORT=50000 \
  --env DB2_DATABASE=TESTDB \
  --env DB2_USERNAME=db2inst1 \
  --env DB2_PASSWORD=password \
  -- uv --directory /path/to/db2-mcp-server run db2-mcp-server
```

**Copy-paste one-liner (replace /path/to/db2-mcp-server with your actual path):**
```bash
claude mcp add --transport stdio db2-mcp-server --env DB2_HOST=localhost --env DB2_PORT=50000 --env DB2_DATABASE=TESTDB --env DB2_USERNAME=db2inst1 --env DB2_PASSWORD=password -- uv --directory /path/to/db2-mcp-server run db2-mcp-server
```

**Example with actual path:**
```bash
# If your project is at /home/user/projects/db2-mcp-server
claude mcp add --transport stdio db2-mcp-server \
  --env DB2_HOST=localhost \
  --env DB2_PORT=50000 \
  --env DB2_DATABASE=TESTDB \
  --env DB2_USERNAME=db2inst1 \
  --env DB2_PASSWORD=password \
  -- uv --directory /home/user/projects/db2-mcp-server run db2-mcp-server
```

**Copy-paste one-liner:**
```bash
claude mcp add --transport stdio db2-mcp-server --env DB2_HOST=localhost --env DB2_PORT=50000 --env DB2_DATABASE=TESTDB --env DB2_USERNAME=db2inst1 --env DB2_PASSWORD=password -- uv --directory /home/user/projects/db2-mcp-server run db2-mcp-server
```

Verify the connection:
```bash
claude mcp list
# Should show: db2-mcp-server - ✓ Connected
```

## Using with Claude Desktop

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
        "/path/to/db2-mcp-server",
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
}
```

**Note**: Replace `/path/to/db2-mcp-server` with your actual project path.

## Running the Server

### STDIO Mode (for MCP clients)
```bash
source .venv/bin/activate
db2-mcp-server --transport stdio
```

### HTTP Mode (for testing)
```bash
source .venv/bin/activate
db2-mcp-server-stream-http
# Server runs on http://127.0.0.1:3721/mcp
```

## MCP Interface

### Tools

The server exposes the following MCP tool:

#### `list_tables`
Lists tables in the DB2 database with optional filtering.

**Parameters:**
- `schema_name` (optional): Filter by schema name
- `table_type` (optional): Filter by table type (e.g., 'T' for tables, 'V' for views)
- `limit` (optional, default: 100): Maximum number of tables to return

**Example usage in Claude:**
> Can you list all tables in the database?
>
> Show me all views in the MYSCHEMA schema

### Prompts

The server provides three built-in prompts:

#### `db2_query_helper`
Generates helpful prompts for DB2 query construction with best practices.

**Parameters:**
- `context` (optional): Additional context for the prompt
- `table_name` (optional): Specific table to focus on

#### `db2_schema_analyzer`
Provides guidance for analyzing DB2 schema structures, relationships, and optimization.

**Parameters:**
- `context` (optional): Additional context for analysis

#### `dynamic_prompt`
Loads custom prompts from JSON configuration files (see Dynamic Prompts section).

**Parameters:**
- `prompt_name` (optional): Name of the dynamic prompt to use
- `context` (optional): Additional context
- `table_name` (optional): Specific table name

### Resources

The server exposes two resources with DB2 reference information:

#### `db2://connection-guide`
Comprehensive guide for DB2 connection configuration, including:
- Environment variable setup
- Connection string formats
- Security best practices

#### `db2://query-templates`
Common DB2 query templates for:
- Basic SELECT queries
- Table and column metadata queries
- Index information
- Table size queries
- Foreign key relationships

**Example usage in Claude:**
> Show me the DB2 connection guide
>
> What query templates are available?

## Dynamic Prompts

The server supports dynamic prompt loading from JSON configuration files. This allows you to customize prompts for specific DB2 query scenarios.

### Example Usage
```bash
export PROMPTS_FILE=/path/to/your/prompts_config.json
db2-mcp-server --transport stdio
```

### Configuration Format
See `examples/prompts_config.json` for a complete example and `docs/DYNAMIC_PROMPTS.md` for detailed documentation.

## Testing

The project includes comprehensive test coverage (**93%**) to ensure reliability.

### Run Tests
```bash
source .venv/bin/activate

# Run all tests with coverage
pytest --cov=src/db2_mcp_server --cov-report=html tests/

# Verbose output with missing coverage
pytest --cov=src/db2_mcp_server --cov-report=term-missing -v
```

### Test Suite Coverage
- Core functionality (`test_core.py`)
- Database tools (`test_list_tables.py`)
- Caching mechanism (`test_cache.py`)
- Logging configuration (`test_logger.py`)
- Dynamic prompt loading (`test_dynamic_loader.py`, `test_integration_dynamic_prompts.py`)
- Storage functionality (`test_table_metadata.py`)

## Security

This server is designed with security in mind:

- **Read-Only Operations**: No INSERT, UPDATE, or DELETE operations allowed
- **Credential Management**: Database credentials stored in environment variables (never in code)
- **Limited Privileges**: Designed to work with read-only database users
- **Structured Logging**: Errors logged in JSON format without exposing sensitive data

### Best Practices
1. Always use a database user with SELECT-only privileges
2. Never commit the `.env` file to version control
3. Use `.env.example` as a template for configuration
4. Enable SSL/TLS for production database connections (configure in connection string)

## Troubleshooting

### DB2 Container Won't Start
```bash
# Check if container is running
docker ps -a | grep db2

# View logs
docker logs db2

# Restart container
docker restart db2
```

### Connection Refused
- Ensure DB2 container has finished initializing (3-5 minutes)
  ```bash
  docker logs db2 2>&1 | grep -i "setup has completed"
  ```
- Check port 50000 is not being used by another service: `lsof -i :50000`
- Verify credentials in `.env` file
- **Verify the database name**: Run `docker exec db2 bash -c "su - db2inst1 -c 'db2 list database directory'"` to check the actual database name (might be `TESTDB` not `SAMPLE`)

### MCP Server Not Connecting in Claude Code
- Use the CLI to add the server: `claude mcp add --transport stdio ...`
- Verify connection: `claude mcp list` should show "✓ Connected"
- Check MCP server health: `claude mcp get db2-mcp-server`

### Import Errors
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
uv sync
```

## Documentation

- **[MCP_SETUP.md](MCP_SETUP.md)**: Complete setup and configuration guide
- **[docs/DYNAMIC_PROMPTS.md](docs/DYNAMIC_PROMPTS.md)**: Dynamic prompts documentation
- **[TABLE_METADATA_GUIDE.md](TABLE_METADATA_GUIDE.md)**: Table metadata feature guide

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure test coverage remains above 90%
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Uses IBM's [ibm_db](https://github.com/ibmdb/python-ibmdb) driver
- Inspired by the [Model Context Protocol](https://modelcontextprotocol.io/)
