# MCP Server + FastAPI

A simple MCP server that connects AI clients to a FastAPI backend.

The project includes:

* FastAPI product APIs
* User registration and login
* Password hashing with bcrypt
* JWT authentication
* JWT scopes for authorization
* MCP tools for product operations
* Streamable HTTP MCP server
* MCP Inspector for testing

## Architecture

```text
AI Agent / MCP Inspector
          |
          | Bearer JWT
          v
    MCP Server :8001
          |
          | HTTP
          v
    FastAPI :8000
          |
          v
      PostgreSQL
```

## Project Structure

```text
mcp-server/
├── .env
├── .gitignore
├── pyproject.toml
├── README.md
├── src/
│   ├── api/
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── create_tables.py
│   │   ├── products/
│   │   └── users/
│   │
│   └── mcp_server/
│       ├── auth.py
│       ├── client.py
│       └── server.py
└── uv.lock
```

## Environment

Create `.env` in the project root:

```env
JWT_SECRET=your-secret-key
```

Do not commit `.env`.

## Install Dependencies

```bash
uv sync
```

## Run FastAPI

From the project root:

```bash
uv run uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

FastAPI:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Run MCP Server

Open another terminal:

```bash
uv run uvicorn mcp_server.server:app --host 127.0.0.1 --port 8001 --reload
```

MCP endpoint:

```text
http://127.0.0.1:8001/mcp
```

## Authentication

Users can register through:

```text
POST /create-user
```

Login through:

```text
POST /login
```

Login returns a JWT:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

The JWT contains:

* `sub` — user ID
* `scope` — user permissions
* `iat` — issued time
* `exp` — expiration time

## Scopes

Example:

```text
s_read
→ products:read
```

```text
s_write
→ products:read products:write
```

Available permissions:

```text
products:read
products:write
```

## MCP Tools

### `get_products`

Requires:

```text
products:read
```

### `get_product`

Requires:

```text
products:read
```

### `create_product`

Requires:

```text
products:write
```

## MCP Inspector

Start Inspector:

```bash
npx @modelcontextprotocol/inspector
```

Connect using:

```text
Transport: Streamable HTTP
URL: http://127.0.0.1:8001/mcp
```

Add the JWT as an HTTP header:

```text
Authorization: Bearer YOUR_JWT
```

Then the available MCP tools can be tested directly from Inspector.

## Development

Run both servers in separate terminals:

### Terminal 1

```bash
uv run uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

### Terminal 2

```bash
uv run uvicorn mcp_server.server:app --host 127.0.0.1 --port 8001 --reload
```

### Terminal 3 — Inspector

```bash
npx @modelcontextprotocol/inspector
```

## Authentication Flow

```text
User
 ↓
POST /login
 ↓
JWT
 ↓
MCP Client / Inspector
 ↓
Authorization: Bearer JWT
 ↓
MCP Server
 ↓
Verify JWT
 ↓
Check scope
 ↓
MCP Tool
 ↓
FastAPI API
 ↓
Database
```
