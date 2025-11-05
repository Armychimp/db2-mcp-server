#!/bin/bash

# Test the MCP server via HTTP mode
# This doesn't require an IDE connection

echo "Starting MCP server in HTTP mode..."
echo "Server will run on http://127.0.0.1:3721"
echo ""
echo "In another terminal, you can test with curl:"
echo ""
echo "  # Check the root path"
echo "  curl http://127.0.0.1:3721"
echo ""

export DB2_HOST=localhost
export DB2_PORT=50000
export DB2_DATABASE=TESTDB
export DB2_USERNAME=db2inst1
export DB2_PASSWORD=password

source .venv/bin/activate
db2-mcp-server-stream-http
