---
title: BeeAI Workshop Lab 2
description: Create a multi-agent ACP workflow
logo: images/ibm-blue-background.png
---

# Create a Multi-Agent ACP Workflow

In this lab, we'll create a ticket agent that uses the triage agent and the response agent in a single workflow.

## Steps

### 1. Open the Project Directory

If you don't already have the `intro_acp_beeai` folder open in VS Code, navigate there. Your working directory should look something like this: `~/beeai-workshop`.

### 2. Install Dependencies

If you already did this in Lab 1, you can skip this step. If not, open your terminal (either in VS Code or using your preferred terminal) and install the dependencies:

```shell
uv sync
```

### 3. Run the agents

In your terminal, run all the agents (open 3 windows/tabs):

```shell
uv run src/ticket_triage_agent.py
```

```shell
uv run src/ticket_response_agent.py
```

```shell
uv run src/ticket_workflow_agent.py
```

### 4. Verify All Agents Are Running

In your browser navigate to:

- [http://localhost:8000/docs](http://localhost:8000/docs)
- [http://localhost:8001/docs](http://localhost:8001/docs)
- [http://localhost:8002/docs](http://localhost:8002/docs)

1. Pull down **GET** `/agents` *List Agents*
2. Hit the `Try it out` button and then click `Execute`

**Expected Results:**

Under `Responses` you should see the corresponding agent listed.

**Try the curl command:** In a new terminal window, run:

```shell
curl -X 'GET' 'http://localhost:8000/agents' -H 'accept: application/json'
```

### 5. Execute the Ticket Workflow Agent

#### Option A: Use a curl command

In a separate terminal, run this curl command:

```shell
curl -N -X POST http://localhost:8002/runs \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"agent_name":"ticket_workflow_agent","input":[{"parts":[{"content":"Hi there, this is Jane Doe. Ever since yesterday your ProPlan keeps throwing \"Error 500\" whenever I try to export reports. This is blocking my quarter-end close—please fix ASAP or refund the month.AccountNumber: 872-55","content_encoding":"plain","content_url":null}]}],"mode":"stream"}'
```

#### Option B: Use your browser to use the FastAPI interface

1. In your browser navigate to [http://localhost:8002/docs](http://localhost:8002/docs)
2. Pull down **POST** `/runs` *Create Run*
3. Hit the `Try it out` button
4. In the `Request body`:

   - Find **"agent_name"** and change the value from "string" to **"ticket_workflow_agent"**
   - Find **"content"** and change the value from "string" to:

     ```text
     Hi there, this is Jane Doe. Ever since yesterday your ProPlan won't let me export reports. This is blocking my quarter-end close—please fix ASAP or refund the month.AccountNumber: 872-55
     ```

   - Remove the **"content_url"** line
   - Find **"mode"** and change the value from "sync" to **"stream"**

5. Click `Execute`
6. Scroll down to the server response

**Expected Results:**

You should see both the triage output (structured data about the ticket) and the response output (a human-like customer service response) in the server response.

### 6. Clean Up

Stop the ACP agent servers using `Ctrl + C` or exiting the terminal where it is running.
