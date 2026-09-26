# MCP Server and Product API

A Python service with two HTTP applications:

- A FastAPI product API backed by PostgreSQL.
- An MCP server that exposes product operations as tools and verifies access tokens with Auth0.

The MCP server listens on port `8001` and forwards product requests to the API on port `8000`.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL
- An Auth0 tenant and API configured to issue access tokens for the MCP resource
- Node.js and npm/npx if you want to use MCP Inspector

## Configuration

Create a `.env` file in the repository root:

```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/mcp_server
AUTH0_DOMAIN=your-tenant.us.auth0.com
AUTH0_AUDIENCE=https://your-api-identifier
```

`AUTH0_DOMAIN` is the Auth0 tenant domain without `https://`. `AUTH0_AUDIENCE` must match the identifier configured for your Auth0 API. The code uses this value as the MCP resource and validates incoming bearer tokens against it. Keep `.env` private and do not commit credentials.

The MCP transport configuration in `src/mcp_server/server.py` currently includes a development ngrok hostname in its allowed hosts/origins and OAuth metadata. Update those values there if you expose the server under a different public hostname.

## Install

From the repository root:

```bash
uv sync
```

## Initialize the database

Create the PostgreSQL database named in `DATABASE_URL`, then create the product table:

```bash
uv run python -m api.create_tables
```

## Run the services

Start the product API in one terminal:

```bash
uv run uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

Start the MCP server in a second terminal:

```bash
uv run uvicorn mcp_server.server:app --host 127.0.0.1 --port 8001 --reload
```

The API provides interactive documentation at <http://127.0.0.1:8000/docs>. The MCP endpoint is <http://127.0.0.1:8001/mcp>.

## Product API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | API health/cover response |
| `POST` | `/create-product` | Create a product |
| `GET` | `/retrieve-all-products` | List products |
| `GET` | `/retrieve-product/{product_id}` | Retrieve a product by UUID |

Example create request:

```json
{
  "product_name": "Example product",
  "price": 25,
  "description": "A sample product",
  "quantity": 4
}
```

`quantity` must be greater than zero. The API does not currently add authentication middleware; MCP tool access is protected by Auth0 token verification and scope checks.

## MCP tools and scopes

The server exposes these tools:

| Tool | Required scope | Description |
| --- | --- | --- |
| `get_products` | `products:read` | List all products |
| `get_product` | `products:read` | Get one product by ID |
| `create_product` | `products:write` | Create a product |

Configure the Auth0 API and clients to issue the required scopes. Requests to the MCP endpoint must include an Auth0 access token as a bearer token.

## Test with MCP Inspector

Run Inspector:

```bash
npx @modelcontextprotocol/inspector
```

Connect with the Streamable HTTP transport and URL `http://127.0.0.1:8001/mcp`. Provide an Auth0 access token with the needed scope when prompted by the client, or configure the Inspector request header as:

```text
Authorization: Bearer <access-token>
```

The MCP application also publishes OAuth protected-resource and authorization-server metadata under `/.well-known/` routes. These metadata routes currently use a development Auth0 tenant and ngrok resource URL configured in `src/mcp_server/server.py`; update them for your deployment.

## Project layout

```text
src/
├── api/
│   ├── main.py                 # FastAPI product API
│   ├── database.py             # SQLAlchemy engine and session
│   ├── create_tables.py        # Database table initialization
│   └── products/
│       ├── models.py
│       ├── routes.py
│       └── schemas.py
└── mcp_server/
    ├── auth0.py                # Auth0 integration and token verifier
    └── server.py               # MCP tools, OAuth metadata, HTTP app
```
