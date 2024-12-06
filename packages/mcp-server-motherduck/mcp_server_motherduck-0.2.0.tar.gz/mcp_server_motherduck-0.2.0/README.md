# mcp-server-motherduck MCP server

A MCP server for MotherDuck and local DuckDB 

## Components

### Resources

### Prompts

The server implements one prompt:
- duckdb-motherduck-initial-prompt: A prompt to initialize a connection to duckdb or motherduck and start working with it

### Tools

The server implements three tools:
- initialize-connection: Create a connection to either a local DuckDB or MotherDuck and retrieve available databases
  - Takes "type" (DuckDB or MotherDuck) as input
- read-schemas: Get table schemas from a specific DuckDB/MotherDuck database
  - Takes "database_name" as required string arguments
- execute-query: Execute a query on the MotherDuck (DuckDB) database
  - Takes "query" as required string arguments

## Configuration Claude Desktop

Add the snippet below to your Claude Desktop config and make sure to set the HOME var to your home folder (needed by DuckDB). 

When using MotherDuck, you also need to set a [MotherDuck token](https://motherduck.com/docs/key-tasks/authenticating-and-connecting-to-motherduck/authenticating-to-motherduck/#storing-the-access-token-as-an-environment-variable) env var.

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Published Servers Configuration</summary>
  ```
  "mcpServers": {
    "mcp-server-motherduck": {
      "command": "uvx",
      "args": [
        "mcp-server-motherduck"
      ],
      "env": {
        "motherduck_token": "",
        "HOME": ""
      }
    }
  }
  ```
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "mcp-server-motherduck": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/<username>/mcp-server/mcp-server-motherduck",
        "run",
        "mcp-server-motherduck"
      ]
    }
  }
  ```
</details>

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /Users/<username>/mcp-server/mcp-server-motherduck run mcp-server-motherduck
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.
