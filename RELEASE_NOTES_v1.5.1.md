# Release Notes - v1.5.1

## 🐛 Bug Fixes

### Fixed MCP Connection Hanging Issues
- **Problem**: MCP server would get stuck showing "HTTP ✓ MCP ✗" and require multiple disconnect/reconnect cycles
- **Solution**: Implemented proper cleanup and state management for smooth connections

### Key Improvements:
1. **Added `/disconnect` endpoint** - Properly cleans up all pending requests when plugin disconnects
2. **Improved connection state tracking** - Both plugin and MCP activity monitored with timeouts
3. **Fixed pending state display** - Now correctly shows "HTTP: ... MCP: ..." during connection attempts
4. **Smooth reconnection** - No more hanging or stuck states when reconnecting

## 🧪 Testing Framework Added
- Comprehensive Jest test suite for TypeScript
- Unit tests for all critical components
- Integration tests for connection flows
- Test runner scripts for easy testing

## 📋 For Users

### Updating to v1.5.1

Due to npx caching, users need to explicitly specify the version:

```json
{
  "mcpServers": {
    "robloxstudio-mcp": {
      "command": "npx",
      "args": ["-y", "robloxstudio-mcp@1.5.1"],
      "description": "Advanced Roblox Studio integration for AI assistants"
    }
  }
}
```

Or use `@latest`:
```json
"args": ["-y", "robloxstudio-mcp@latest"]
```

### Plugin Update
The Roblox Studio plugin has been updated with:
- Proper disconnect notifications
- Improved connection state display
- Better error handling

**Important**: Download and install the new plugin file from this release.

## 🔧 Technical Details

### Server Changes:
- `BridgeService.clearAllPendingRequests()` - Force cleanup method
- Plugin activity tracking (10-second timeout)
- MCP activity tracking (15-second timeout)
- Proper state synchronization

### Plugin Changes:
- Calls `/disconnect` endpoint on disconnect
- Shows correct pending states during connection
- Resets connection counters properly

## 📦 Installation

### NPM Package:
```bash
npm install -g robloxstudio-mcp@1.5.1
# or
npx robloxstudio-mcp@1.5.1
```

### Roblox Studio Plugin:
1. Download `MCPPlugin.rbxmx` from this release
2. Open Roblox Studio
3. Navigate to Plugins tab
4. Click "Plugins Folder"
5. Place the .rbxmx file in the folder
6. Restart Studio

## 🚀 What's Next
- Continue monitoring connection stability
- Consider FastMCP migration for future versions
- Add more comprehensive error reporting

## 📝 Full Changelog
- Fix: MCP connection hanging issues
- Fix: Proper cleanup on disconnect
- Fix: Connection state display
- Add: Comprehensive test suite
- Add: Test documentation
- Update: Plugin disconnect behavior
- Update: Connection state tracking

---

**Note**: After updating, restart Claude Desktop to ensure the new version is loaded.