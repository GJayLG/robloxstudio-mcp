# NPX Caching Issue Solution

## Problem
When users run `npx robloxstudio-mcp`, npx may use a cached version instead of downloading the latest version from npm.

## Why This Happens
NPX caches packages to improve performance. When you run `npx robloxstudio-mcp`, it:
1. Checks if the package exists in the npx cache
2. If found, uses the cached version
3. Only downloads if not in cache or if forced

## Solutions for Users

### Option 1: Force Latest Version (Recommended)
```bash
npx robloxstudio-mcp@latest
```
or
```bash
npx robloxstudio-mcp@1.5.1
```

### Option 2: Clear NPX Cache
```bash
# Clear the entire npx cache
npx clear-npx-cache

# Or manually clear the specific package
rm -rf ~/.npm/_npx/*/node_modules/robloxstudio-mcp
```

### Option 3: Use --ignore-existing Flag
```bash
npx --ignore-existing robloxstudio-mcp
```

### Option 4: Install Globally
```bash
# Install globally
npm install -g robloxstudio-mcp

# Then run directly
robloxstudio-mcp
```

## For MCP Configuration

Update your Claude Desktop config to force the latest version:

```json
{
  "mcpServers": {
    "robloxstudio-mcp": {
      "command": "npx",
      "args": ["-y", "robloxstudio-mcp@latest"],
      "description": "Advanced Roblox Studio integration for AI assistants"
    }
  }
}
```

Or specify the exact version:

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

## Best Practice for Updates

When releasing updates, always inform users to:

1. **Update their MCP config** to specify `@latest` or the new version number
2. **Restart Claude Desktop** after updating the config
3. **Clear npx cache** if they continue to see old behavior

## Alternative: Direct npm Install

For users who frequently update, installing directly might be better:

```bash
# Install the package
npm install -g robloxstudio-mcp

# Update MCP config to use direct command
{
  "mcpServers": {
    "robloxstudio-mcp": {
      "command": "robloxstudio-mcp",
      "args": [],
      "description": "Advanced Roblox Studio integration for AI assistants"
    }
  }
}

# To update later
npm update -g robloxstudio-mcp
```

This avoids npx caching issues entirely.