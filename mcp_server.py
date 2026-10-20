"""MCP Server for Concurrency Semaphore Guard.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import ConcurrencySemaphoreGuard

guard = ConcurrencySemaphoreGuard()

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "acquire",
                                "description": "Acquire concurrency lease and verify RPM quotas",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "lease_id": {"type": "string"}
                                    },
                                    "required": ["lease_id"]
                                }
                            },
                            {
                                "name": "release",
                                "description": "Release held concurrency lease",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "lease_id": {"type": "string"}
                                    },
                                    "required": ["lease_id"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                call_name = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if call_name == "acquire":
                    res = guard.acquire(args.get("lease_id", ""))
                elif call_name == "release":
                    res = guard.release(args.get("lease_id", ""))
                else:
                    res = {"error": "Unknown tool"}
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
