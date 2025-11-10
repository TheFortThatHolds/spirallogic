"""Connector stubs for SOULbox Spirit outbound actions."""

from .api_client import APIClientConnector
from .mcp_bridge import MCPBridgeConnector
from .ui_automation import UIAutomationConnector
from .local_llm import LocalLLMConnector

__all__ = [
    "APIClientConnector",
    "MCPBridgeConnector",
    "UIAutomationConnector",
    "LocalLLMConnector",
]
