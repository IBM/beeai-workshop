---
title: Use the BeeAI Platform
description: Run the BeeAI Platform and use your agents in the UI
logo: images/ibm-blue-background.png
---

# Interact with Your Agents in the BeeAI Platform

In this lab, we'll run our TicketWorkflow that we created in Lab 2 in the BeeAI platform. The BeeAI platform creates a simple and elegant UI so that we can test, run, and share our agents easily.

## Steps

### 1. Open the Project Directory

If you don't already have the `intro_acp_beeai` folder open in VS Code, navigate there. Your working directory should look something like this: `~/beeai-workshop/intro_acp_beeai`.

### 2. Install Dependencies

If you already did this in Lab 1 or 2, you can skip this step. If not, open your terminal (either in VS Code or using your preferred terminal) and install the dependencies:

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

### 4. Launch the BeeAI UI

You should have already installed, started, and set up your LLM provider in the BeeAI Platform by following the Workshop Specific Requirements section of the Pre-Work. If you have not, please go back and follow them before proceeding.

In your terminal, run:

```shell
beeai ui
```

You should see the UI launch in your browser.

!!! insight
    If you navigate to the menu bar on the left hand side you will see a list of agents. All 3 agents that we are running on the active server appear because they each have UI metadata in their agent detail. If we killed the server, these agents would instantly disappear.

### 5. Run the ticket_workflow_agent in the BeeAI Platform

1. Navigate to the menu bar on the left hand side and select the ticket_workflow_agent
2. Enter in the sample text or have fun with coming up with your own ticket:

    ```text
    Hi there, this is Jane Doe. Ever since yesterday your ProPlan won't let me export reports. This is blocking my quarter-end close—please fix ASAP or refund the month.AccountNumber: 872-55
    ```

3. Press run

**Expected Results:**

You should see both the triage output (structured data about the ticket) and the response output (a human-like customer service response) in the platform interface.

### 6. Clean Up

1. Stop the ACP agent servers using `Ctrl + C` or exiting the terminal where it is running.
2. Clean up the platform by running this command in your terminal:

    ```shell
    beeai platform delete
    ```

## Congratulations! You've completed the Introduction to ACP + BeeAI Workshop.