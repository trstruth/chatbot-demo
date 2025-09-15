#!/usr/bin/env python3
"""
Minimal Azure OpenAI chat over stdin/stdout using only stdlib.

Environment variables required:
  - AZURE_OPENAI_API_KEY:       Your Azure OpenAI API key
  - AZURE_OPENAI_ENDPOINT:      Your Azure OpenAI endpoint, e.g. https://my-resource.openai.azure.com
  - AZURE_OPENAI_DEPLOYMENT:    Your deployed model name (deployment ID)
  - AZURE_OPENAI_API_VERSION:   Optional, defaults to 2024-07-01-preview

Usage:
  $ export AZURE_OPENAI_API_KEY=... 
  $ export AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com
  $ export AZURE_OPENAI_DEPLOYMENT=<your-deployment-name>
  $ python3 chat_azure_openai.py

Type messages and press Enter. Type 'exit' or 'quit' to leave, 'reset' to clear history.
"""

import json
import os
import sys
from urllib import request, error
import ssl

context = ssl._create_unverified_context()


def _require_env(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(2)
    return val


def chat_completion(messages):
    """Call Azure OpenAI Chat Completions and return assistant content.

    messages: list of {role: str, content: str}
    returns: str (assistant content)
    """
    api_key = _require_env("AZURE_OPENAI_API_KEY")
    endpoint = _require_env("AZURE_OPENAI_ENDPOINT").rstrip("/")
    deployment = _require_env("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-07-01-preview")

    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }
    payload = {
        "messages": messages,
        # Keep it simple and predictable; tweak as needed.
        "temperature": 0.2,
        # Non-streaming for simplicity; easier stdout handling.
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers=headers, method="POST")
    try:
        with request.urlopen(req, context=context) as resp:
            body = resp.read().decode("utf-8")
            obj = json.loads(body)
    except error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        print(f"HTTP {e.code} error calling Azure OpenAI: {detail}", file=sys.stderr)
        raise
    except error.URLError as e:
        print(f"Network error calling Azure OpenAI: {e}", file=sys.stderr)
        raise

    choices = obj.get("choices") or []
    if not choices:
        raise RuntimeError(f"No choices in response: {obj}")

    message = choices[0].get("message") or {}
    content = message.get("content")
    if content is None:
        # Handle tool/function-call style responses defensively.
        content = json.dumps(message, ensure_ascii=False)
    return content


def main():
    # Minimal system prompt; adjust if desired.
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    print("Azure OpenAI Chat (type 'exit' to quit, 'reset' to clear)")
    while True:
        try:
            user = input("You> ").strip()
        except EOFError:
            print()  # newline on Ctrl-D
            break
        except KeyboardInterrupt:
            print()  # newline on Ctrl-C
            break

        if not user:
            continue
        if user.lower() in {"exit", "quit"}:
            break
        if user.lower() == "reset":
            messages = [{"role": "system", "content": "You are a helpful assistant."}]
            print("(history cleared)")
            continue

        messages.append({"role": "user", "content": user})
        try:
            reply = chat_completion(messages)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            # Remove the last user message to keep history consistent on failure.
            messages.pop()
            continue

        messages.append({"role": "assistant", "content": reply})
        print("Assistant>", reply)


if __name__ == "__main__":
    main()

