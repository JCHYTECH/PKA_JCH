#!/usr/bin/env python3

import json
import os
import select
import signal
import subprocess
import threading


class McpStdioClient:
    def __init__(self):
        env = os.environ.copy()
        env["NODE_OPTIONS"] = "--dns-result-order=ipv6first"
        self.process = subprocess.Popen(
            ["/bin/bash", "/Users/jchavauxm5/PKA_JCH/scripts/mcp_ha_lupo_readonly.sh"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
            start_new_session=True,
        )
        self.stderr = []
        threading.Thread(target=self.drain_stderr, daemon=True).start()
        self.next_id = 1

    def drain_stderr(self):
        for line in self.process.stderr:
            self.stderr.append(line.rstrip())
            del self.stderr[:-30]

    def send(self, message):
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def request(self, method, params=None, timeout=60):
        request_id = self.next_id
        self.next_id += 1
        message = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            message["params"] = params
        self.send(message)
        while True:
            ready, _, _ = select.select([self.process.stdout], [], [], timeout)
            if not ready:
                raise TimeoutError(f"MCP request timed out: {method}")
            line = self.process.stdout.readline()
            if not line:
                raise RuntimeError(f"MCP proxy exited with code {self.process.poll()}")
            response = json.loads(line)
            if response.get("id") != request_id:
                continue
            if "error" in response:
                raise RuntimeError(f"{method}: {response['error'].get('message', 'MCP error')}")
            return response.get("result", {})

    def close(self):
        if self.process.poll() is None:
            os.killpg(self.process.pid, signal.SIGTERM)
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(self.process.pid, signal.SIGKILL)
            self.process.wait(timeout=5)


def main():
    client = McpStdioClient()
    try:
        initialized = client.request(
            "initialize",
            {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "pka-readonly-probe", "version": "1.0"},
            },
        )
        client.send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        tools = client.request("tools/list")
        resources = client.request("resources/list")
        print(json.dumps({
            "server": initialized.get("serverInfo"),
            "protocol": initialized.get("protocolVersion"),
            "tools": tools.get("tools"),
            "resources": resources.get("resources"),
        }, ensure_ascii=False, indent=2))

        names = {tool["name"] for tool in tools.get("tools", [])}
        if "homeassistant__GetLiveContext" in names:
            result = client.request(
                "tools/call",
                {"name": "homeassistant__GetLiveContext", "arguments": {"domain": "sensor"}},
            )
            print(json.dumps({"live_context": result}, ensure_ascii=False, indent=2))
        for resource in resources.get("resources", []):
            if resource.get("uri") == "homeassistant://assist/context-snapshot":
                result = client.request("resources/read", {"uri": resource["uri"]})
                print(json.dumps({"context_resource": result}, ensure_ascii=False, indent=2))
    finally:
        client.close()


if __name__ == "__main__":
    main()
