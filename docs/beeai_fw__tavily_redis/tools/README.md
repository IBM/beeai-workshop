---
title: Create Tools
description: Create the tools to enable the AI agent
logo: images/BeeAI-Logo-White.png
---


# Tool Development: Tavily Internet Search + Redis RAG

> ⚠️ **Before you begin:**  
> Make sure you have completed the [Prework](../pre-work/README.md) and [Setup](../setup/README.md) instructions.  
> The tools rely on environment configuration, the redis stack to be running, dependencies, and your `.env` file.

In this section of the workshop, you'll build two essential tools that power your company assistant:

1. **Web Search Tool** using a locally run **Tavily MCP server**
2. **Redis Retriever Tool** for enabling **Retrieval-Augmented Generation (RAG)** from your vector database

Each tool is implemented interactively. You’ll fill in missing logic and test each script on its own before integrating it into your assistant.

---

## Part 1: Tavily MCP Tool

### Step 1: Verify Your Environment

1. **Navigate to the correct directory:**

    ```bash
    cd beeai-workshop/beeai_fw_tavily_redis
    ```

2. **Install dependencies:**

    ```bash
    uv sync
    ```

### Step 2: Locate the Tool File

1. Navigate to the following file:

    ```text
    src/tavily_mcp_tool.py
    ```

2. Some parts of the implementation are left incomplete for you to **fill-in-the-blank** and complete the tool. Follow the in-line comments to complete the logic. If you need help, check the solution:

    ```text
    src/solutions/tavily_mcp_tool.py
    ```

### Step 3: Run the Tool

- Run or debug the Tavily tool independently to test its functionality:

    ```bash
    uv run src/tavily_mcp_tool.py
    ```

> Remember to save the file with your changes before running it!

---

## Part 2: Redis Retriever Tool

### Step 1: Verify Your Environment

- If you've just completed Part 1, your environment should still be active. Otherwise:

    ```bash
    cd beeai-workshop/beeai_fw_tavily_redis
    uv sync
    ```

### Step 2: Locate the Tool File

1. Navigate to:

    ```text
    src/redis_retriever.py
    ```

2. Some parts of the implementation are left incomplete for you to **fill-in-the-blank** and complete the tool. Follow the in-line comments to complete the logic. If you need help, check the solution:

    ```text
    src/solutions/redis_retriever.py
    ```

### Step 3: Run the Tool

- Run or debug your Redis retriever tool independently:

    ```bash
    uv run src/redis_retriever.py
    ```

> Remember to save the file with your changes before running it!

    This ensures the tool works as expected before integrating it into your BeeAI Agent!
