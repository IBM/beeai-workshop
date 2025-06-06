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

#### API Key

- [OpenAI](https://platform.openai.com/api-keys) API key (paid) or [Groq](https://console.groq.com/keys) API key (free)

## BeeAI Platform

Install BeeAI platform using the [installation instructions in the documentation](https://docs.beeai.dev/introduction/installation). Don't forget to run `beeai platform start` to start the platform prior to running the examples.

Already installed BeeAI in the past? Be sure to update it to the latest version according to the instructions in the documentation.

## Workshop Specific Requirements

1. Get the workshop code:

    Option A: Clone with Git (Recommended):

    ```shell
    git clone https://github.com/IBM/beeai-workshop.git
    ```

    Option B: Download ZIP:
    If you're not comfortable with Git, [download the ZIP file](https://github.com/IBM/beeai-workshop/archive/refs/heads/main.zip) and extract it to your desired location.

2. Navigate to the workshop folder and open in VS Code:

    ```shell
    cd beeai-workshop/intro_acp_beeai
    code .
    ```

    !!! important
        Make sure to open the specific `intro_acp_beeai` folder in VS Code, not the entire `beeai-workshop` directory. This ensures proper project structure and dependencies.

    **Alternative:** You can also open VS Code first, then use "File > Open Folder" to navigate to and select the `beeai-workshop/intro_acp_beeai` folder.

3. Create a .env file based on the env.template file at the intro_acp_beeai directory level. Uncomment out either the OpenAI API Key or the Groq API key and add your own api.

    ```shell
    cp env.template .env
    ```

    !!! note
        For OpenAI you just need the API Key, for Groq you need to uncomment all 3 environment variables but only need to modify the API Key.
