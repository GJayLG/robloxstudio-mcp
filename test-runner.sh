#!/bin/bash

# Roblox Studio MCP Server Test Runner
# This script runs the test suite with various options

echo "🧪 Roblox Studio MCP Server Test Suite"
echo "======================================"

# Check if npm packages are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Parse command line arguments
case "$1" in
    "watch")
        echo "👁️  Running tests in watch mode..."
        npm run test:watch
        ;;
    "coverage")
        echo "📊 Running tests with coverage..."
        npm run test:coverage
        echo ""
        echo "📈 Coverage report generated in ./coverage directory"
        echo "   Open ./coverage/lcov-report/index.html in a browser to view"
        ;;
    "specific")
        if [ -z "$2" ]; then
            echo "❌ Please specify a test file pattern"
            echo "   Example: ./test-runner.sh specific bridge"
            exit 1
        fi
        echo "🎯 Running specific tests matching: $2"
        npx jest --testNamePattern="$2"
        ;;
    "debug")
        echo "🐛 Running tests in debug mode..."
        NODE_OPTIONS='--inspect-brk' npx jest --runInBand
        ;;
    "quick")
        echo "⚡ Running quick smoke tests..."
        npx jest --testNamePattern="should return health status|should handle plugin ready|should handle complete connection lifecycle"
        ;;
    *)
        echo "🏃 Running all tests..."
        npm test
        ;;
esac

echo ""
echo "✅ Test run complete!"