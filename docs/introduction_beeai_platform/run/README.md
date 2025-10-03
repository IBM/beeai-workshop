---
title: Use the BeeAI Platform
description: Run the BeeAI Platform and use your agents in the UI
logo: images/ibm-blue-background.png
---

# Interact with your agents in the BeeAI Platform

In this lab, we'll run our agent in the BeeAI platform. The BeeAI platform creates a simple and elegant UI so that we can test, run, and share our agents easily.

## Steps

### 1. Install BeeAI Platform

Install BeeAI platform using the [installation instructions in the documentation](https://docs.beeai.dev/introduction/installation).

Already installed BeeAI in the past? Be sure to update it to the latest version according to the instructions in the documentation.

### 2. Start the BeeAI Platform (optionally with Phoenix enabled)

BeeAI includes OpenTelemetry instrumentation to collect traces and metrics. Telemetry data helps with performance monitoring, error tracking, usage analytics, and debugging agent interactions.

> Important License Notice: Phoenix is disabled by default in BeeAI. When you enable Phoenix, be aware that Arize Phoenix is licensed under the Elastic License v2 (ELv2), which has specific terms regarding commercial use and distribution. By enabling Phoenix, you acknowledge that you are responsible for ensuring compliance with the ELv2 license terms for your specific use case. Please review the Phoenix license before enabling this feature in production environments.

To start the BeeAI Platform with Arize Phoenix, run:

```shell
beeai platform start --set phoenix.enabled=true
```

To start the BeeAI Platform without Arize Phoenix, run:

```shell
beeai platform start
```

### 3. Launch the BeeAI UI

In your terminal, run:

```shell
beeai ui
```

You should be prompted to select a model provider and model. For running locally, Ollama and Granite 3.3 are recommended.

You should see the UI launch in your browser.

!!! insight
    If you navigate to the menu bar on the left hand side you will see a list of agents. These example agents come with BeeAI Platform.  We'll add our custom agent in steps that follow.

### 4. Open the project directory

If you don't already have the `intro_beeai_platform` folder open in VS Code, navigate there. Your working directory should look something like this: `~/beeai-workshop/intro_beeai_platform`.

### 5. Install dependencies

Open your terminal (either in VS Code or using your preferred terminal) and install the dependencies:

```shell
uv sync
```

### 6. Review your .env file

Review your `.env` file to ensure you copied the env.template and have the settings you need.

### 7. Serve the agent

In your terminal, run the agent:

```shell
uv run src/agent.py
```

!!! insight
    If you take a look at the code pay special attention to the metadata in the `@server.agent` decorator. The metadata is used by the BeeAI Platform UI.

### 8. Run the agent

1. Navigate to the menu bar on the left hand side and select the Conference Prep Agent

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
        * Look under "All" and not "Root"
    * source citations (not always present)

### 8. Clean Up

1. Stop the 3 agent servers using `Ctrl + C` or exiting the terminal where it is running.
2. Clean up the platform by running this command in your terminal:

    ```shell
    beeai platform delete
    ```

## Congratulations! You've completed the Introduction to BeeAI Platform workshop.