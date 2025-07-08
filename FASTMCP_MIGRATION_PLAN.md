# FastMCP Migration Plan

## Overview
FastMCP is a Python-based MCP framework, which means migrating from the current TypeScript implementation would require a complete rewrite.

## Key Differences

### Current Implementation (TypeScript)
- Uses `@modelcontextprotocol/sdk` 
- Custom HTTP server with Express
- Manual connection management
- Bridge service for request/response handling
- Complex state management for plugin/MCP coordination

### FastMCP (Python)
- Simplified server creation with decorators
- Built-in transport handling (STDIO, HTTP, SSE)
- Automatic connection management
- More robust error handling
- Production-ready features out of the box

## Migration Steps

### 1. Environment Setup
```bash
# Install Python dependencies
pip install fastmcp
pip install aiohttp  # For HTTP server functionality
```

### 2. Basic Server Structure
```python
from fastmcp import FastMCP
import json
import aiohttp
from aiohttp import web

# Initialize FastMCP server
mcp = FastMCP("Roblox Studio MCP")

# Add custom HTTP endpoints for plugin communication
app = web.Application()
plugin_connected = False
pending_requests = {}
```

### 3. Tool Migration Example
```python
# Current TypeScript tool
# async getFileTree(path: string) { ... }

# FastMCP equivalent
@mcp.tool
async def get_file_tree(path: str = "") -> dict:
    """Get complete hierarchy of the Roblox Studio project"""
    # Forward request to plugin via HTTP
    request_id = await bridge_request("get_file_tree", {"path": path})
    return await wait_for_response(request_id)
```

### 4. HTTP Bridge Integration
```python
# Plugin communication endpoints
async def handle_poll(request):
    """Handle plugin polling for requests"""
    global pending_requests
    
    if not mcp_connected:
        return web.json_response({
            "error": "MCP server not connected",
            "mcpConnected": False
        }, status=503)
    
    # Get oldest pending request
    if pending_requests:
        request_id, request_data = pending_requests.popitem()
        return web.json_response({
            "requestId": request_id,
            "request": request_data,
            "mcpConnected": True
        })
    
    return web.json_response({
        "request": None,
        "mcpConnected": True
    })

app.router.add_get('/poll', handle_poll)
```

### 5. Connection Management
```python
# FastMCP handles MCP connections automatically
# We only need to manage plugin connections

async def handle_ready(request):
    """Plugin connection notification"""
    global plugin_connected
    plugin_connected = True
    return web.json_response({"success": True})

async def handle_disconnect(request):
    """Plugin disconnection cleanup"""
    global plugin_connected, pending_requests
    plugin_connected = False
    pending_requests.clear()
    return web.json_response({"success": True})
```

## Benefits of Migration

### 1. **Simplified Code**
- Decorator-based tool registration
- Automatic parameter validation
- Built-in error handling

### 2. **Better Connection Stability**
- FastMCP handles reconnection logic
- Built-in timeout management
- Cleaner state management

### 3. **Production Features**
- Built-in authentication
- OpenAPI generation
- Better testing support

### 4. **Reduced Complexity**
- No manual MCP protocol handling
- Automatic transport management
- Simpler request/response flow

## Challenges

### 1. **Language Change**
- Complete rewrite required
- Python deployment considerations
- Different ecosystem (pip vs npm)

### 2. **Performance**
- Python may have different performance characteristics
- Async handling differences

### 3. **Deployment**
- Users need Python installed
- Different packaging/distribution method
- May need to bundle Python runtime

## Hybrid Approach Alternative

Instead of full migration, consider a hybrid approach:

1. **Keep TypeScript HTTP server** for plugin communication
2. **Use FastMCP Python server** for MCP protocol
3. **Connect them via HTTP/WebSocket**

```
[Roblox Plugin] <-> [TS HTTP Server] <-> [FastMCP Python Server] <-> [Claude]
```

This would:
- Maintain existing plugin compatibility
- Get FastMCP benefits for MCP handling
- Allow gradual migration

## Recommendation

Given the significant architectural change, I recommend:

1. **First**: Fix current connection issues in TypeScript (already done)
2. **Evaluate**: Test if current fixes resolve stability issues
3. **Prototype**: Create a small FastMCP proof-of-concept
4. **Decide**: Based on results, either:
   - Stick with improved TypeScript version
   - Migrate fully to Python
   - Implement hybrid approach

The connection fixes we just implemented may resolve most issues without needing a full rewrite.