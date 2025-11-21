---
title: Agent Stack
description: Run the Agent Stack and use your agents in the UI
logo: images/BeeAI-Logo-White.png
---

# Interact with your agents using Agent Stack

Agent Stack is an open, self-hostable infrastructure for deploying AI agents built with any framework. A Linux Foundation project built on the Agent2Agent Protocol (A2A), Agent Stack gives you everything needed to move agents from local development to shared production environments—without vendor lock-in.

## What Agent Stack provides

Agent Stack provides everything you need to deploy and operate agents in production:

* Self-hostable server to run your agents
* Web UI for testing and sharing deployed agents
* CLI for deploying and managing agents
* Runtime services your agents can access:

    * LLM Service — Switch between 15+ providers (Anthropic, OpenAI, watsonx.ai, Ollama) without code changes
    * Embeddings & vector search for RAG and semantic search
    * File storage — S3-compatible uploads/downloads
    * Document text extraction via Docling
    * External integrations via MCP protocol (APIs, Slack, Google Drive, etc.) with OAuth
    * Secrets management for API keys and credentials
* SDK (`agentstack-sdk`) for standardized A2A service requests
* HELM charts for Kubernetes deployments with customizable storage, databases, and auth

## Lab

### 1. Install Agent Stack

Install Agent Stack using the [installation instructions in the documentation](https://agentstack.beeai.dev/introduction/quickstart#installation).

#### Follow the "One-Line Install"

To install a specific version of Agent Stack, set the `AGENTSTACK_VERSION` environment variable before running the install script.  For example:

```bash
sh -c "$(AGENTSTACK_VERSION=0.4.1 curl -LsSf https://raw.githubusercontent.com/i-am-bee/agentstack/HEAD/install.sh)"
```

### 2. Start the Agent Stack (optionally with Phoenix and Docling enabled)

Agent Stack includes OpenTelemetry instrumentation to collect traces and metrics. Telemetry data helps with performance monitoring, error tracking, usage analytics, and debugging agent interactions.

> Important License Notice: Phoenix is disabled by default in Agent Stack. When you enable Phoenix, be aware that Arize Phoenix is licensed under the Elastic License v2 (ELv2), which has specific terms regarding commercial use and distribution. By enabling Phoenix, you acknowledge that you are responsible for ensuring compliance with the ELv2 license terms for your specific use case. Please review the Phoenix license before enabling this feature in production environments.

* To start the Agent Stack with Arize Phoenix use `--set phoenix.enabled=true`
* To start the Agent Stack with Docling use `--set docling.enabled=true`

```shell
agentstack platform start --set phoenix.enabled=true --set docling.enabled=true
```

### 3. Launch the UI

In your terminal, run:

```shell
agentstack ui
```

You should be prompted to select a model provider and model if you did not already set these.
For this lab, use Ollama and `ibm/granite4:micro-h` for the language model.

You should see the UI launch in your browser.

!!! insight
    If you navigate to the menu bar on the left hand side you will see a list of agents. These example agents come with Agent Stack.  We'll add our custom agent in steps that follow.

### 4. Serve the agent

In your terminal, run the agent:

```shell
uv --directory agentstack run src/agent.py
```

!!! insight
    If you take a look at the code pay special attention to the metadata in the `@server.agent` decorator. The metadata is used by the UI.

### 5. Run the agent

1. Navigate to the menu bar on the left hand side of the UI and select the Conference Prep Agent. You might need to refresh the page.

2. Notice that we build a form UI.

    * `Task` is the main input to the agent.
    * `Company name` is especially useful if your task doesn't mention the company name
    * `Style` suggests the type of output you want. `detailed` is typically longer and may include source citations. `list` is a good option if you like bullet points.
    * The `Event` name and `Event date` are used here primarily for UI demo purposes.

3. Experiment with the different form fields. Try using one of the following tasks:

    * Brief me for a Shopify meeting at the conference. Give me an overview of the company, some recent news about them, and anything important I need to know from our internal notes.

    * I'm planning on meeting the Moderna rep at the next conference. Remind me where we left off on previous discussions.

    * Build a security talking sheet for Siemens Energy. How does their strategy compare to their competitors'?

4. Try different inputs.

5. Explore:

    * the trajectory steps (look in "How did I get this answer?")
    * the captured details in Arize Phoenix
        * browse to `http://localhost:6006/`
        * open project "default"
        * Select "All" (not Root Spans)
        * Most details show up after the run
        * Look under "All" and not "Root"
    * source citations (not always present)
