---
title: BeeAI Workshop Lab 1
description: Create and invoke ACP agents
logo: images/ibm-blue-background.png
---

# Create and invoke ACP agents

In this lab, you will invoke 2 agents using the ACP SDK (the Python code is provided). One agent is written using the BeeAI Framework and the other agent is written using PydanticAI. We are using 2 different frameworks to illustrate how easy it is to make any agent ACP-compatible.

**Agent Overview:**

- **Agent 1 (BeeAI Framework)**: "Triage Agent" – categorizes the ticket (e.g., billing, tech, complaint) and extracts key facts in a structured way (e.g., using tags, severity, sentiment).
- **Agent 2 (PydanticAI)**: "Response Agent" – takes the structured summary and crafts a tone-specific response (e.g., empathetic for complaints, efficient for billing).

!!! prerequisite
    The following steps assume that you have already completed the pre-work section. If not, please return to the previous section before moving forward.

## Steps

### 1. Open the Project Directory

If you don't already have the `intro_acp_beeai` folder open in VS Code, navigate there. Your working directory should look something like this: `~/beeai-workshop/intro_acp_beeai`.

### 2. Install Dependencies

Open your terminal (either in VS Code or using your preferred terminal) and install the dependencies:

```shell
uv sync
```

### 3. Run the Ticket Triage Agent

In your terminal, run the ticket triage agent (defaults to run on port 8000):

```shell
uv run src/ticket_triage_agent.py
```

!!! insight
    If you take a look at the code you will notice that the agent is wrapped in an `@server.agent` decorator. The decorator makes it an ACP agent and the metadata provides agent details for discoverability.

### 4. Test the Agent via Browser Interface

Use your browser to invoke the `ticket_triage_agent` using the FastAPI interface:

1. In your preferred browser navigate to [http://localhost:8000/docs](http://localhost:8000/docs)
2. Pull down **GET** `/agents` *List Agents*
3. Hit the `Try it out` button and then click `Execute`

**Expected Results:**

Under `Responses`:

- Under `Response body`, the result shows just one agent named `ticket_triage_agent` (the second agent is not running on port 8000).
- Under `Curl`, you get the curl command that you can run in a terminal (instead of using the UI)

**Try the curl command:** In a new terminal window, run:

```shell
curl -X 'GET' 'http://localhost:8000/agents' -H 'accept: application/json'
```

!!! insight
    This shows you that your ACP agent is discoverable on port 8000 and if you had more than one agent running on this server you could use the `GET /agents` command to list them.

!!! note
    To terminate the ACP agent server press `Ctrl + C` in the terminal where the server is running or close the terminal.

### 5. Run the Ticket Response Agent

In a separate terminal, run the ticket response agent (defaults to run on port 8001):

```shell
uv run src/ticket_response_agent.py
```

!!! insight
    Notice how the `ticket_triage_agent` and `ticket_response_agent` are running on separate ports. Agents can either have their own server and be discoverable on multiple ports or be on the same server (as you'll see in lab 2).

### 6. Invoke the Response Agent

Invoke the response agent using a curl command. Remember that the `ticket_response_agent` expects a formatted output from the `ticket_triage_agent` as its input. You'll put these together in a sequential workflow in lab 2.

In a separate terminal, run this curl command:

```shell
curl -N -X POST http://localhost:8001/runs \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"agent_name":"ticket_response_agent","input":[{"parts":[{"content":"{\"category\":[\"Technical\"],\"customer_name\":\"Jane Doe\",\"account_id\":\"872-55\",\"product\":\"ProPlan\",\"issue_summary\":\"ProPlan product is throwing \\\"Error 500\\\" when exporting reports since yesterday, blocking quarter-end close.\",\"severity\":\"high\",\"sentiment\":\"negative\",\"incident_date\":\"2024-06-11\"}","content_encoding":"plain","content_url":null}]}],"mode":"stream"}'
```

**Expected Results:**

In the response body, you should see an appropriate human-like ticket agent response.


### 7. Clean Up

If you have not already, remember to stop the ACP agent servers using `Ctrl + C` or exiting the terminal where they are running.