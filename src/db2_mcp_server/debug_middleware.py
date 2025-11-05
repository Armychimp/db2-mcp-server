"""Debug middleware for MCP server to log all requests and responses."""

import logging
import json
from functools import wraps
from typing import Any

logger = logging.getLogger(__name__)


def log_mcp_call(func):
    """Decorator to log MCP function calls with full details."""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        logger.debug(f"=== MCP Call: {func.__name__} ===")
        logger.debug(f"Args: {args}")
        logger.debug(f"Kwargs: {kwargs}")

        try:
            result = await func(*args, **kwargs)
            logger.debug(f"Result type: {type(result)}")
            logger.debug(f"Result: {result}")
            return result
        except Exception as e:
            logger.error(f"MCP call failed: {func.__name__}", exc_info=True)
            raise

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        logger.debug(f"=== MCP Call: {func.__name__} ===")
        logger.debug(f"Args: {args}")
        logger.debug(f"Kwargs: {kwargs}")

        try:
            result = func(*args, **kwargs)
            logger.debug(f"Result type: {type(result)}")
            logger.debug(f"Result: {result}")
            return result
        except Exception as e:
            logger.error(f"MCP call failed: {func.__name__}", exc_info=True)
            raise

    # Detect if function is async or sync
    import inspect
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def wrap_mcp_methods(mcp_instance):
    """Wrap MCP instance methods with debug logging."""
    methods_to_wrap = [
        'list_tools',
        'call_tool',
        'list_prompts',
        'get_prompt',
        'list_resources',
        'read_resource',
    ]

    for method_name in methods_to_wrap:
        if hasattr(mcp_instance, method_name):
            original_method = getattr(mcp_instance, method_name)
            wrapped_method = log_mcp_call(original_method)
            setattr(mcp_instance, method_name, wrapped_method)
            logger.debug(f"Wrapped MCP method: {method_name}")


def enable_debug_middleware(mcp_instance):
    """Enable debug middleware on the MCP instance."""
    logger.info("Enabling MCP debug middleware")
    wrap_mcp_methods(mcp_instance)
