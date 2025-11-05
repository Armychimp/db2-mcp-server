#!/usr/bin/env python3
"""
Test the MCP server via STDIO transport (simulates how an IDE would connect).

This script starts the MCP server as a subprocess and communicates with it
using JSON-RPC over STDIO, exactly like Claude Code or bobide would.

Usage:
    python test_via_stdio.py
"""

import subprocess
import json
import sys
import os

def send_jsonrpc_request(process, method, params=None):
    """Send a JSON-RPC request to the MCP server."""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }

    # Write request to stdin
    request_str = json.dumps(request) + "\n"
    process.stdin.write(request_str)
    process.stdin.flush()

    # Read response from stdout
    response_str = process.stdout.readline()
    if not response_str:
        return None

    return json.loads(response_str)

def main():
    print("=" * 70)
    print("Testing DB2 MCP Server via STDIO (like an IDE would)")
    print("=" * 70)

    # Set up environment
    env = os.environ.copy()
    env.update({
        "DB2_HOST": "localhost",
        "DB2_PORT": "50000",
        "DB2_DATABASE": "TESTDB",
        "DB2_USERNAME": "db2inst1",
        "DB2_PASSWORD": "password"
    })

    # Start the MCP server
    cmd = ["uv", "--directory", "/home/armychimp/AI/db2-mcp-server",
           "run", "db2-mcp-server", "--transport", "stdio"]

    print("\nStarting server:", " ".join(cmd))
    print()

    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env
        )

        # Test 1: Initialize
        print("1. Sending initialize request...")
        response = send_jsonrpc_request(process, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })

        if response and "result" in response:
            print("   ✓ Server initialized")
            print(f"   Server info: {response['result'].get('serverInfo', {})}")
        else:
            print("   ✗ Initialize failed")
            print(f"   Response: {response}")

        # Test 2: List tools
        print("\n2. Listing tools...")
        response = send_jsonrpc_request(process, "tools/list")

        if response and "result" in response:
            tools = response['result'].get('tools', [])
            print(f"   ✓ Found {len(tools)} tool(s)")
            for tool in tools:
                print(f"   - {tool['name']}")

                # Check for the required field in schema
                input_schema = tool.get('inputSchema', {})
                defs = input_schema.get('$defs', {})
                list_tables_input = defs.get('ListTablesInput', {})

                if 'required' in list_tables_input:
                    print(f"     ✓ Schema has 'required' field: {list_tables_input['required']}")
                else:
                    print(f"     ✗ Schema missing 'required' field")

                print(f"     Schema preview: {json.dumps(list_tables_input.get('properties', {}), indent=6)[:200]}...")
        else:
            print("   ✗ List tools failed")
            print(f"   Response: {response}")

        # Test 3: Call the tool
        print("\n3. Calling list_tables tool...")
        response = send_jsonrpc_request(process, "tools/call", {
            "name": "list_tables",
            "arguments": {
                "schema_name": "",
                "limit": 5
            }
        })

        if response and "result" in response:
            print("   ✓ Tool called successfully")
            content = response['result'].get('content', [])
            if content:
                print(f"   Result preview: {str(content[0])[:200]}...")
        else:
            print("   ✗ Tool call failed")
            print(f"   Response: {response}")

        # Cleanup
        process.terminate()
        process.wait(timeout=5)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)
    print("Testing Complete")
    print("=" * 70)

if __name__ == "__main__":
    main()
