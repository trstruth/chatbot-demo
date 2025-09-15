Azure OpenAI Minimal Chat (stdin/stdout)

This repository includes a tiny, dependency-free Python script that connects to an Azure OpenAI deployed model, reads user input from stdin, and prints model responses to stdout.

Files
- `chat_azure_openai.py`: Minimal chat loop using the Azure OpenAI Chat Completions REST API via Python stdlib.

Prerequisites
- Python 3.8+
- An Azure OpenAI resource with a deployed model (deployment name).
- Your Azure OpenAI endpoint and API key.

Environment
Set these environment variables before running:

- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your endpoint, e.g. `https://my-resource.openai.azure.com`
- `AZURE_OPENAI_DEPLOYMENT`: Your deployment name (the model deployment ID)
- `AZURE_OPENAI_API_VERSION` (optional): Defaults to `2024-07-01-preview`

Run
```
export AZURE_OPENAI_API_KEY=YOUR_KEY
export AZURE_OPENAI_ENDPOINT=https://YOUR_RESOURCE.openai.azure.com
export AZURE_OPENAI_DEPLOYMENT=YOUR_DEPLOYMENT

python3 chat_azure_openai.py
```

Usage
- Type your message and press Enter.
- Type `reset` to clear the conversation history.
- Type `exit` or `quit` to leave the chat.

Notes
- The script uses the REST API directly with Python stdlib (no extra packages).
- For streaming tokens or SDK-based usage, this script can be extended, but this minimal version returns full responses for simplicity.

