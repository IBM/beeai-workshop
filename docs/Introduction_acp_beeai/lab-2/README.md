---
title: BeeAI Workshop Lab 2
description: Create a multi-agent ACP workflow
logo: images/ibm-blue-background.png
---

# Create a ticket agent with triage and response

In this lab, we'll create a ticket agent that uses the triage agent and the response agent in a single workflow.

## Steps

### 1. Open the Project Directory

If you don't already have the `intro_acp_beeai` folder open in VS Code, navigate there. Your working directory should look something like this: `~/beeai-workshop/intro_acp_beeai`.

### 2. Install Dependencies

If you already did this in Lab 1, you can skip this step. If not, open your terminal (either in VS Code or using your preferred terminal) and install the dependencies:

```shell
uv sync
```

### 3. Run the Ticket Workflow Agent

In your terminal, run the ticket workflow agent (defaults to run on port 8000):

```shell
uv run src/ticket_workflow_agent.py
```

!!! insight
    If you take a look at the code you will notice that there are 3 ACP agents in this `ticket_workflow_agent.py` file. The main agent, named "TicketWorkflow", orchestrates the run of the `ticket_triage_agent` and `ticket_response_agent` sequentially and returns both of their outputs. The `ticket_triage_agent` runs first and then its output is used as the input for the `ticket_response_agent`.

### 4. Verify All Agents Are Running

In your browser navigate to [http://localhost:8000/docs](http://localhost:8000/docs):

1. Pull down **GET** `/agents` *List Agents*
2. Hit the `Try it out` button and then click `Execute`

**Expected Results:**

Under `Responses` you should see all 3 agents listed! This is because all 3 agents are running on the same port.

**Try the curl command:** In a new terminal window, run:

```shell
curl -X 'GET' 'http://localhost:8000/agents' -H 'accept: application/json'
```

### 5. Execute the Ticket Workflow Agent

#### Option A: Use a curl command

In a separate terminal, run this curl command:

```shell
curl -N -X POST http://localhost:8000/runs \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"agent_name":"TicketWorkflow","input":[{"parts":[{"content":"Hi there, this is Jane Doe. Ever since yesterday your ProPlan keeps throwing \"Error 500\" whenever I try to export reports. This is blocking my quarter-end close—please fix ASAP or refund the month.AccountNumber: 872-55","content_encoding":"plain","content_url":null}]}],"mode":"stream"}'
```

#### Option B: Use your browser to use the FastAPI interface

1. In your browser navigate to [http://localhost:8000/docs](http://localhost:8000/docs)
2. Pull down **POST** `/runs` *Create Run*
3. Hit the `Try it out` button
4. In the `Request body`:
   - Find **"agent_name"** and change the value from "string" to **"TicketWorkflow"**
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