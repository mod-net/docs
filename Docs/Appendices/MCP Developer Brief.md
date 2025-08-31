# MCP Quick Dev Reference

## Lifecycle

1. **Client → initialize**
2. **Server → InitializeResult**
3. **Client → notifications/initialized**
4. Normal bidirectional JSON-RPC
5. Transport closes to end

## Transports

* **STDIO:** one JSON per line, no literal newlines in payloads. Log to stderr only.
* **HTTP + SSE (single endpoint):**

  * POST JSON-RPC. Response is JSON or SSE stream of JSON messages.
  * Optional GET opens receive-only SSE stream.
  * Headers: `Mcp-Session-Id` after init, `MCP-Protocol-Version` on every request.
  * Validate `Origin` for local servers. Bind 127.0.0.1 by default.

## Initialize

```json
// request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "tools": { "listChanged": true },
      "prompts": { "listChanged": true },
      "resources": { "subscribe": true, "listChanged": true },
      "logging": {},
      "experimental": {}
    },
    "clientInfo": { "name": "YourClient", "version": "x.y.z" }
  }
}
```

```json
// result
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "tools": { "listChanged": true },
      "prompts": { "listChanged": false },
      "resources": { "subscribe": true, "listChanged": true },
      "logging": {}
    },
    "serverInfo": { "name": "YourServer", "version": "x.y.z" },
    "instructions": "Optional human-readable setup notes"
  }
}
```

```json
// then a notification (no id)
{ "jsonrpc": "2.0", "method": "notifications/initialized", "params": {} }
```

## Common Shapes

```json
// Error (JSON-RPC)
{ "jsonrpc": "2.0", "id": 1, "error": { "code": -32602, "message": "Invalid params", "data": {} } }
```

```json
// Content blocks used in tool results, resources, prompts, sampling
[
  { "type": "text", "text": "..." , "annotations": { "audience": "assistant|user", "priority": 0.8 } },
  { "type": "image", "data": "<base64>", "mimeType": "image/png" },
  { "type": "audio", "data": "<base64>", "mimeType": "audio/wav" },
  { "type": "resource_link", "uri": "file:///path", "name": "optional", "mimeType": "text/plain" }
]
// When you also return structured JSON:
{ "structuredContent": { /* your JSON */ } }
```

## Tools

```json
// tools/list request
{ "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": { "cursor": "opt" } }
```

```json
// tools/list result
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "search",
        "title": "Search",
        "description": "Query web index",
        "inputSchema": { "type": "object", "required": ["q"], "properties": { "q": { "type": "string" }, "limit": { "type": "integer" } } },
        "outputSchema": { "type": "object", "properties": { "results": { "type": "array" } } }
      }
    ],
    "nextCursor": null
  }
}
```

```json
// tools/call request
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": { "name": "search", "arguments": { "q": "rust jsonrpc", "limit": 5 } }
}
```

```json
// tools/call result (success or logical error via isError)
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [ { "type": "text", "text": "Top 5 results..." } ],
    "structuredContent": { "results": [ /* ... */ ] },
    "isError": false
  }
}
```

```json
// tools/list_changed notification (if advertised)
{ "jsonrpc": "2.0", "method": "notifications/tools/list_changed", "params": {} }
```

## Prompts

```json
// prompts/list
{ "jsonrpc": "2.0", "id": 4, "method": "prompts/list", "params": { "cursor": "opt" } }
```

```json
// prompts/list result
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "prompts": [
      {
        "name": "summarize",
        "title": "Summarize Document",
        "description": "Summarize provided text",
        "arguments": [
          { "name": "text", "description": "Input text", "required": true }
        ]
      }
    ],
    "nextCursor": null
  }
}
```

```json
// prompts/get
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "prompts/get",
  "params": {
    "name": "summarize",
    "arguments": { "text": "..." }
  }
}
```

```json
// prompts/get result
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "messages": [
      { "role": "system", "content": [ { "type": "text", "text": "You are a helpful summarizer." } ] },
      { "role": "user", "content": [ { "type": "text", "text": "{{text}}" } ] }
    ]
  }
}
```

```json
// prompts/list_changed
{ "jsonrpc": "2.0", "method": "notifications/prompts/list_changed", "params": {} }
```

## Resources

```json
// Resource descriptor
{
  "uri": "file:///path/to/file.txt",
  "name": "file.txt",
  "mimeType": "text/plain",
  "description": "Optional",
  "annotations": { "audience": "assistant", "priority": 0.7 }
}
```

```json
// resources/list
{ "jsonrpc": "2.0", "id": 6, "method": "resources/list", "params": { "cursor": "opt" } }
```

```json
// resources/list result
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": { "resources": [ /* descriptor */ ], "nextCursor": null }
}
```

```json
// resources/read
{ "jsonrpc": "2.0", "id": 7, "method": "resources/read", "params": { "uri": "file:///path/to/file.txt" } }
```

```json
// resources/read result
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "uri": "file:///path/to/file.txt",
    "mimeType": "text/plain",
    "contents": [ { "type": "text", "text": "file body..." } ]
  }
}
```

```json
// resources/subscribe
{ "jsonrpc": "2.0", "id": 8, "method": "resources/subscribe", "params": { "uri": "file:///path/to/file.txt" } }
```

```json
// notifications/resources/updated
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": { "uri": "file:///path/to/file.txt", "title": "opt" }
}
```

```json
// notifications/resources/list_changed
{ "jsonrpc": "2.0", "method": "notifications/resources/list_changed", "params": {} }
```

## Client Features (server calls these)

### Sampling

```json
// sampling/createMessage (server → client)
{
  "jsonrpc": "2.0",
  "id": 9,
  "method": "sampling/createMessage",
  "params": {
    "messages": [
      { "role": "system", "content": [ { "type": "text", "text": "You are helpful." } ] },
      { "role": "user", "content": [ { "type": "text", "text": "Explain MCP." } ] }
    ],
    "hints": { "modelFamilies": ["gpt","claude"] },
    "preferences": { "intelligencePriority": 0.8, "speedPriority": 0.2 },
    "maxTokens": 512
  }
}
```

```json
// sampling/createMessage result
{
  "jsonrpc": "2.0",
  "id": 9,
  "result": {
    "message": { "role": "assistant", "content": [ { "type": "text", "text": "..." } ] },
    "model": "resolved-model-id",
    "stopReason": "endOfTurn"
  }
}
```

### Elicitation

```json
// elicitation/create (server → client)
{
  "jsonrpc": "2.0",
  "id": 10,
  "method": "elicitation/create",
  "params": {
    "message": { "role": "assistant", "content": [ { "type": "text", "text": "Enter project name:" } ] },
    "requestedSchema": {
      "type": "object",
      "required": ["project"],
      "properties": { "project": { "type": "string", "title": "Project" } }
    }
  }
}
```

```json
// elicitation/create result
{
  "jsonrpc": "2.0",
  "id": 10,
  "result": {
    "action": "accept|decline|cancel",
    "content": { "project": "demo" }
  }
}
```

## Gotchas

* Do not send anything but JSON on STDIO stdout. Newlines delimit messages.
* For HTTP, enforce `Origin`, `Mcp-Session-Id`, `MCP-Protocol-Version`.
* Wait for `initialize` response, then send `notifications/initialized` before any other traffic.
* Use `isError: true` inside tool results for logical failures. Reserve JSON-RPC `error` for protocol failures.
* Support pagination cursors on list endpoints. Return `nextCursor` or null.
* If you stream via SSE, include the final JSON-RPC response event, then end the stream.
