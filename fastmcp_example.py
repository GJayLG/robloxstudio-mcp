"""
Example FastMCP implementation for Roblox Studio MCP Server
This shows how the server would look if migrated to FastMCP
"""

from fastmcp import FastMCP
from aiohttp import web
import asyncio
import uuid
from typing import Dict, Any, Optional

# Initialize FastMCP server
mcp = FastMCP("Roblox Studio MCP", version="1.5.0")

# Global state for plugin communication
plugin_state = {
    "connected": False,
    "last_activity": 0,
    "pending_requests": {},
    "responses": {}
}

# HTTP app for plugin communication
http_app = web.Application()

# === Bridge Functions ===

async def bridge_request(endpoint: str, data: Any) -> str:
    """Send request to plugin and wait for response"""
    request_id = str(uuid.uuid4())
    
    plugin_state["pending_requests"][request_id] = {
        "endpoint": f"/api/{endpoint}",
        "data": data,
        "timestamp": asyncio.get_event_loop().time()
    }
    
    # Wait for response (with timeout)
    timeout = 30  # seconds
    start_time = asyncio.get_event_loop().time()
    
    while request_id not in plugin_state["responses"]:
        if asyncio.get_event_loop().time() - start_time > timeout:
            plugin_state["pending_requests"].pop(request_id, None)
            raise TimeoutError("Plugin request timeout")
        await asyncio.sleep(0.1)
    
    response = plugin_state["responses"].pop(request_id)
    if "error" in response:
        raise Exception(response["error"])
    
    return response

# === FastMCP Tools ===

@mcp.tool
async def get_file_tree(path: str = "") -> Dict[str, Any]:
    """Get complete hierarchy of the Roblox Studio project"""
    result = await bridge_request("file-tree", {"path": path})
    return {"content": [result]}

@mcp.tool 
async def search_files(query: str, search_type: str = "name") -> Dict[str, Any]:
    """Find files by name, type, or content patterns"""
    result = await bridge_request("search-files", {
        "query": query,
        "searchType": search_type
    })
    return {"content": [result]}

@mcp.tool
async def get_script_source(instance_path: str) -> Dict[str, Any]:
    """Get the source code of a script object"""
    result = await bridge_request("get-script-source", {
        "instancePath": instance_path
    })
    return {"content": [result]}

@mcp.tool
async def set_script_source(instance_path: str, source: str) -> Dict[str, Any]:
    """Set the source code of a script object"""
    result = await bridge_request("set-script-source", {
        "instancePath": instance_path,
        "source": source
    })
    return {"content": [result]}

@mcp.tool
async def get_instance_properties(instance_path: str) -> Dict[str, Any]:
    """Get all properties of a specific instance"""
    result = await bridge_request("instance-properties", {
        "instancePath": instance_path
    })
    return {"content": [result]}

@mcp.tool
async def set_property(
    instance_path: str, 
    property_name: str, 
    property_value: Any
) -> Dict[str, Any]:
    """Set a property on any Roblox instance"""
    result = await bridge_request("set-property", {
        "instancePath": instance_path,
        "propertyName": property_name,
        "propertyValue": property_value
    })
    return {"content": [result]}

@mcp.tool
async def create_object(
    class_name: str,
    parent: str,
    name: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new Roblox object instance"""
    result = await bridge_request("create-object", {
        "className": class_name,
        "parent": parent,
        "name": name
    })
    return {"content": [result]}

# === HTTP Endpoints for Plugin ===

async def handle_poll(request):
    """Plugin polls for pending requests"""
    if not plugin_state["connected"]:
        plugin_state["connected"] = True
    
    plugin_state["last_activity"] = asyncio.get_event_loop().time()
    
    # Get oldest pending request
    if plugin_state["pending_requests"]:
        request_id = next(iter(plugin_state["pending_requests"]))
        request_data = plugin_state["pending_requests"].pop(request_id)
        
        return web.json_response({
            "requestId": request_id,
            "request": request_data,
            "mcpConnected": True,
            "pluginConnected": True
        })
    
    return web.json_response({
        "request": None,
        "mcpConnected": True,
        "pluginConnected": True
    })

async def handle_response(request):
    """Plugin sends response for a request"""
    data = await request.json()
    request_id = data["requestId"]
    
    if data.get("error"):
        plugin_state["responses"][request_id] = {"error": data["error"]}
    else:
        plugin_state["responses"][request_id] = data["response"]
    
    return web.json_response({"success": True})

async def handle_ready(request):
    """Plugin connection notification"""
    plugin_state["connected"] = True
    plugin_state["last_activity"] = asyncio.get_event_loop().time()
    return web.json_response({"success": True})

async def handle_disconnect(request):
    """Plugin disconnection"""
    plugin_state["connected"] = False
    plugin_state["pending_requests"].clear()
    plugin_state["responses"].clear()
    return web.json_response({"success": True})

# Configure HTTP routes
http_app.router.add_get('/poll', handle_poll)
http_app.router.add_post('/response', handle_response)
http_app.router.add_post('/ready', handle_ready)
http_app.router.add_post('/disconnect', handle_disconnect)
http_app.router.add_get('/health', lambda r: web.json_response({"status": "ok"}))

# === Main Server Runner ===

async def run_servers():
    """Run both HTTP and MCP servers"""
    # Start HTTP server for plugin
    runner = web.AppRunner(http_app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 3002)
    await site.start()
    print("HTTP server listening on port 3002 for Studio plugin")
    
    # Run MCP server
    # FastMCP can run with different transports:
    # - stdio (default): For Claude Desktop
    # - http: For web-based clients
    # - sse: For server-sent events
    
    # For Claude Desktop, we use stdio
    await mcp.run()

if __name__ == "__main__":
    # Run the servers
    asyncio.run(run_servers())