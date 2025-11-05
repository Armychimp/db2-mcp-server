import logging
import os
import sys
import argparse
import logging

# Third-party imports
from dotenv import load_dotenv
from importlib.metadata import version, PackageNotFoundError

# Local imports
from .logger import setup_logging
from .mcp_instance import mcp

# Setup logging before importing modules
setup_logging()
logger = logging.getLogger(__name__)

# --- Environment Setup ---
load_dotenv()  # Load .env file

# Import modules after mcp instance is created to avoid circular imports
from .tools import list_tables  # Import existing tools
from .prompts import db2_prompts  # Import prompts
from .resources import db2_resources  # Import resources

def main():
  """Entry point for the CLI."""
  parser = argparse.ArgumentParser(
    description="DB2 MCP Server - Read-only MCP server for IBM DB2 databases"
  )
  parser.add_argument(
    "--transport",
    choices=["stdio", "stream_http"],
    default="stdio",
    help="Transport type (stdio or stream_http)",
  )
  parser.add_argument(
    "--debug",
    action="store_true",
    help="Enable debug logging",
  )

  args = parser.parse_args()

  # Enable debug logging if requested
  debug_enabled = args.debug or os.getenv("MCP_DEBUG", "").lower() in ("1", "true", "yes")
  if debug_enabled:
    logging.getLogger().setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug logging enabled")

    # Enable debug middleware for detailed MCP protocol logging
    from .debug_middleware import enable_debug_middleware
    enable_debug_middleware(mcp)
    logger.debug("Debug middleware enabled")

  logger.info(f"Starting DB2 MCP Server")
  logger.info(f"Transport: {args.transport}")
  logger.info(f"DB2_HOST: {os.getenv('DB2_HOST', 'not set')}")
  logger.info(f"DB2_PORT: {os.getenv('DB2_PORT', 'not set')}")
  logger.info(f"DB2_DATABASE: {os.getenv('DB2_DATABASE', 'not set')}")
  logger.info(f"DB2_USERNAME: {os.getenv('DB2_USERNAME', 'not set')}")

  if args.transport == "stream_http":
    # For HTTP transport, use 'streamable-http'
    # Note: host/port are configured in mcp_instance.py
    # Use root path without trailing slash for compatibility
    logger.info(f"Starting streamable-http transport on port {os.getenv('MCP_PORT', '3721')}")
    mcp.run(transport="streamable-http")
  else:
    logger.info("Starting stdio transport")
    mcp.run(transport=args.transport)


def main_stream_http():
  """Run the MCP server with stream_http transport."""
  if "--transport" not in sys.argv:
    sys.argv.extend(["--transport", "stream_http"])
  elif "stream_http" not in sys.argv:
    try:
      idx = sys.argv.index("--transport")
      if idx + 1 < len(sys.argv):
        sys.argv[idx + 1] = "stream_http"
      else:
        sys.argv.append("stream_http")
    except ValueError:
      sys.argv.extend(["--transport", "stream_http"])

  main()


if __name__ == "__main__":
  main()
