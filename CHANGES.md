# MCP Server Connection Fix - v1.5.1

## Issues Fixed

1. **Connection Hanging**: Fixed issue where MCP server would get stuck showing "HTTP ✓ MCP ✗" instead of properly showing pending connection state
2. **Cleanup on Disconnect**: Added proper cleanup of pending requests when disconnecting
3. **State Display**: Fixed status display to show "HTTP: ... MCP: ..." when attempting to connect

## Changes Made

### Server-side (TypeScript)

1. **Added disconnect endpoint** (`/disconnect`) to properly clean up when plugin disconnects
2. **Added `clearAllPendingRequests()` method** to BridgeService to forcefully reject all pending requests
3. **Added plugin activity tracking** to automatically detect disconnected plugins after 10 seconds of inactivity
4. **Fixed polling endpoint** to properly track plugin connection state

### Plugin-side (Lua)

1. **Added disconnect notification** - Plugin now calls `/disconnect` endpoint when disconnecting
2. **Fixed connection state reset** - Connection failure counters are reset on disconnect
3. **Improved status display**:
   - Shows "HTTP: ... MCP: ..." when first connecting
   - Shows "HTTP: OK MCP: ..." when HTTP is connected but waiting for MCP
   - Shows "HTTP: ... MCP: ..." when retrying connection
4. **Better cleanup** on disconnect to prevent hanging connections

## How to Apply

1. The TypeScript changes have been built and are ready in the `dist` folder
2. The plugin.luau changes need to be manually applied to MCPPlugin.rbxmx in Roblox Studio
3. Users should update both the NPM package and the Roblox Studio plugin

## Testing

After applying these changes:
1. Connection should show pending state ("...") for both HTTP and MCP when connecting
2. Disconnect/reconnect should work smoothly without hanging
3. No lingering processes should remain after disconnect