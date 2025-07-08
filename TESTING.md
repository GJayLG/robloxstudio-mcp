# Testing Guide for Roblox Studio MCP Server

## Overview

This project uses **Jest** as the testing framework with **TypeScript** support. The test suite covers:
- Unit tests for individual components
- Integration tests for the complete MCP flow
- Connection management and recovery scenarios
- Request/response handling

## Quick Start

### Install Dependencies
```bash
npm install
```

### Run All Tests
```bash
npm test
```

### Run Tests in Watch Mode
```bash
npm run test:watch
# or
./test-runner.sh watch
```

### Run Tests with Coverage
```bash
npm run test:coverage
# or
./test-runner.sh coverage
```

## Test Structure

```
src/
├── __tests__/
│   ├── bridge-service.test.ts    # Unit tests for BridgeService
│   ├── http-server.test.ts       # HTTP server endpoint tests
│   └── integration.test.ts       # Full integration tests
```

## Test Scenarios Covered

### 1. Connection Management (`http-server.test.ts`)
- ✅ Plugin connection lifecycle
- ✅ MCP server state tracking
- ✅ Connection timeout handling
- ✅ Pending state display ("HTTP: ... MCP: ...")

### 2. Disconnect/Cleanup (`bridge-service.test.ts`)
- ✅ Clearing pending requests on disconnect
- ✅ Request timeout handling
- ✅ Force cleanup functionality
- ✅ Connection recovery

### 3. Request/Response Flow (`integration.test.ts`)
- ✅ Complete request/response cycle
- ✅ Error handling
- ✅ Multiple concurrent requests
- ✅ Request prioritization (oldest first)

### 4. Edge Cases
- ✅ Reconnection after disconnect
- ✅ Timeout scenarios
- ✅ Plugin inactivity detection
- ✅ MCP server inactivity detection

## Running Specific Tests

### Using Jest directly:
```bash
# Run tests matching a pattern
npx jest --testNamePattern="connection"

# Run a specific test file
npx jest src/__tests__/bridge-service.test.ts

# Run tests in a specific describe block
npx jest --testNamePattern="BridgeService.*Request Management"
```

### Using the test runner script:
```bash
# Run specific tests
./test-runner.sh specific "connection"

# Run quick smoke tests
./test-runner.sh quick

# Debug tests (with Node debugger)
./test-runner.sh debug
```

## Testing the Connection Fixes

The test suite specifically validates the recent connection fixes:

### 1. **Disconnect Cleanup Test**
```typescript
test('should clear pending requests on disconnect', async () => {
  // Verifies that all pending requests are cleared when plugin disconnects
});
```

### 2. **Connection State Display Test**
```typescript
test('should show correct pending states during connection', async () => {
  // Verifies "HTTP: ... MCP: ..." display during connection attempts
});
```

### 3. **Reconnection Test**
```typescript
test('should handle disconnect and reconnect gracefully', async () => {
  // Verifies smooth reconnection without hanging
});
```

## Manual Testing Checklist

After running automated tests, perform these manual checks:

1. **Connection Flow**
   - [ ] Start MCP server (`npm run dev`)
   - [ ] Open Roblox Studio plugin
   - [ ] Click Connect - verify "HTTP: ... MCP: ..." appears
   - [ ] Verify connection completes to "HTTP: OK MCP: OK"

2. **Disconnect/Reconnect**
   - [ ] Click Disconnect in plugin
   - [ ] Verify clean disconnection
   - [ ] Click Connect again
   - [ ] Verify no hanging or stuck states

3. **Error Recovery**
   - [ ] Stop MCP server while connected
   - [ ] Verify plugin shows appropriate error state
   - [ ] Restart MCP server
   - [ ] Verify automatic recovery or manual reconnect works

## Debugging Tests

### Enable Jest Debugging
```bash
# Run with Node debugger
NODE_OPTIONS='--inspect-brk' npx jest --runInBand

# Then attach your debugger (VS Code, Chrome DevTools, etc.)
```

### Verbose Output
```bash
# Show detailed test output
npx jest --verbose

# Show console.log statements
npx jest --no-silent
```

## Coverage Reports

After running `npm run test:coverage`:
- Terminal shows coverage summary
- HTML report: `./coverage/lcov-report/index.html`
- Coverage includes:
  - Statement coverage
  - Branch coverage
  - Function coverage
  - Line coverage

## CI/CD Integration

Add to your CI pipeline:
```yaml
# Example GitHub Actions
- name: Run tests
  run: npm test

- name: Generate coverage
  run: npm run test:coverage

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Writing New Tests

### Test Template
```typescript
describe('Component/Feature Name', () => {
  let component: ComponentType;

  beforeEach(() => {
    // Setup
  });

  afterEach(() => {
    // Cleanup
  });

  describe('Specific Functionality', () => {
    test('should do something specific', async () => {
      // Arrange
      const input = 'test';
      
      // Act
      const result = await component.method(input);
      
      // Assert
      expect(result).toBe('expected');
    });
  });
});
```

### Best Practices
1. Use descriptive test names
2. Follow AAA pattern (Arrange, Act, Assert)
3. Test edge cases and error conditions
4. Use `beforeEach` for common setup
5. Clean up resources in `afterEach`
6. Mock external dependencies when needed

## Troubleshooting

### Common Issues

1. **Tests timing out**
   - Increase timeout: `jest.setTimeout(30000)`
   - Check for unresolved promises

2. **Import errors**
   - Ensure `tsconfig.json` is configured correctly
   - Check module resolution settings

3. **Async test failures**
   - Always use `async/await` for asynchronous tests
   - Ensure all promises are resolved

### Getting Help

- Check test output for specific error messages
- Run tests in verbose mode for more details
- Use the debugger to step through failing tests
- Check the Jest documentation: https://jestjs.io/docs/

## Next Steps

1. Run the test suite: `npm test`
2. Check coverage: `npm run test:coverage`
3. Fix any failing tests
4. Add more tests as you add features
5. Integrate into your CI/CD pipeline