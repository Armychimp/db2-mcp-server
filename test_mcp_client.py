#!/usr/bin/env python3
"""
Simple MCP client to test the db2-mcp-server without an IDE.

Usage:
    source .venv/bin/activate
    python test_mcp_client.py
"""

import asyncio
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_mcp_server():
    """Test the MCP server by importing and calling it directly."""
    print("=" * 60)
    print("Testing DB2 MCP Server")
    print("=" * 60)

    # Import the MCP instance
    from src.db2_mcp_server.mcp_instance import mcp
    from src.db2_mcp_server.tools import list_tables
    from src.db2_mcp_server.prompts import db2_prompts
    from src.db2_mcp_server.resources import db2_resources

    # Test 1: List Tools
    print("\n1. Testing tools...")
    tools = await mcp.list_tools()
    print(f"   Found {len(tools)} tool(s):")
    for tool in tools:
        print(f"   - {tool.name}: {tool.description[:80]}...")

        # Check schema for required field
        schema = tool.inputSchema
        list_tables_def = schema.get('$defs', {}).get('ListTablesInput', {})
        if 'required' in list_tables_def:
            print(f"     ✓ Schema has 'required' field: {list_tables_def['required']}")
        else:
            print(f"     ✗ Schema missing 'required' field")

    # Test 2: Call the list_tables tool
    print("\n2. Testing list_tables tool...")
    from src.db2_mcp_server.tools.list_tables import ListTablesInput

    # Create a mock context
    class MockContext:
        pass

    ctx = MockContext()

    try:
        result = await mcp.call_tool("list_tables", {"schema_name": "", "table_type": "", "limit": 5}, ctx)
        print(f"   ✓ Tool executed successfully")
        print(f"   Result: {result[:200]}..." if len(str(result)) > 200 else f"   Result: {result}")
    except Exception as e:
        print(f"   ✗ Tool failed: {e}")

    # Test 3: List Prompts
    print("\n3. Testing prompts...")
    prompts = await mcp.list_prompts()
    print(f"   Found {len(prompts)} prompt(s):")
    for prompt in prompts:
        print(f"   - {prompt.name}: {prompt.description[:80] if prompt.description else 'No description'}...")

    # Test 4: List Resources
    print("\n4. Testing resources...")
    resources = await mcp.list_resources()
    print(f"   Found {len(resources)} resource(s):")
    for resource in resources:
        print(f"   - {resource.name} ({resource.uri})")

    # Test 5: Read a resource
    print("\n5. Testing resource read...")
    try:
        resource_content = await mcp.read_resource("db2://connection-guide")
        print(f"   ✓ Resource read successfully")
        content_preview = str(resource_content)[:200]
        print(f"   Preview: {content_preview}...")
    except Exception as e:
        print(f"   ✗ Resource read failed: {e}")

    print("\n" + "=" * 60)
    print("Testing Complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
