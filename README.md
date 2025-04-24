# MCP Server Saillogger

A server for handling Saillogger data.

## Development Setup

1. Ensure you have Python 3.12+ installed
2. Install `uv` if you haven't already:
   ```bash
   pip install uv
   ```
3. Create and activate a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows
   ```
4. Install dependencies:
   ```bash
   uv pip install -e .
   ```

## Usage

Run the server:
```bash
mcp-server-saillogger
```

# Saillogger AIS MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/introduction) server that provides real-time AIS positions from the Saillogger network into AI applications.

