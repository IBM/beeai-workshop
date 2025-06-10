---
title: BeeAI Workshop Pre-work
description: Preparation for the BeeAI Workshop
logo: images/ibm-blue-background.png
---

# Pre-work

## ACP

### Prerequisites to get started with ACP

#### Visual Studio Code (Recommended)

- You can use any IDE, but this workshop assumes you're using [VS Code](https://code.visualstudio.com/Download)
- If this is your first time using VS Code, make sure to install the Python extension from the extension marketplace

#### uv

- `uv` is the recommended Python package and environment manager for this workshop
- If you're unfamiliar with `uv`, check out [this uv primer](https://agentcommunicationprotocol.dev/introduction/uv-primer) for installation instructions

#### BeeAI Platform

Install BeeAI platform using the [installation instructions in the documentation](https://docs.beeai.dev/introduction/installation). Don't forget to run `beeai platform start` to start the platform prior to running the examples.

Already installed BeeAI in the past? Be sure to update it to the latest version according to the instructions in the documentation.

#### API Key

BeeAI platform needs an API key for a LLM provider to run agents. If you do not have one, we recommend getting a free one on [Groq](https://console.groq.com/keys) by logging in with Google / GitHub. (If you already use an LLM provider, BeeAI probably supports it too -- OpenAI, Ollama, Anthropic, etc.)

Run `beeai env setup` and go through the setup wizard to enter your API key there.

## Workshop Specific Requirements

1. Get the workshop code:

    Option A: Clone with Git (Recommended):

    ```shell
    git clone https://github.com/JanPokorny/beeai-workshop.git
    ```

    Option B: Download ZIP:
    If you're not comfortable with Git, [download the ZIP file](https://github.com/JanPokorny/beeai-workshop/archive/refs/heads/main.zip) and extract it to your desired location.

2. Open the folder in VS Code (use "File > Open Folder" to navigate to and select the `beeai-workshop` folder.)
