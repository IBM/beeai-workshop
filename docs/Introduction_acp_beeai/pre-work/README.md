---
title: BeeAI Workshop Pre-work
description: Preparation for the BeeAI Workshop
logo: images/ibm-blue-background.png
---

# Pre-work

## ACP

### Prerequisites to get started with ACP

#### Python >=3.11

- Go to [python.org/downloads](https://www.python.org/downloads/)
- Download the version for your operating system (Windows, macOS, or Linux)

    !!! important
        During installation, make sure to check the box that says `Add Python to PATH` or manually add it if you skip this step

- To verify installation type `python --version`

#### Visual Studio Code (Recommended)

- You can use any IDE, but this workshop assumes you're using [VS Code](https://code.visualstudio.com/Download)
- If this is your first time using VS Code, make sure to install the Python extension from the extension marketplace

#### uv

- uv is the recommended package and environment manager for this workshop, but you can use uv, pip, or another package manager if you're more comfortable with them.
- If you're unfamiliar with uv, check out [this uv primer](https://agentcommunicationprotocol.dev/introduction/uv-primer) for installation instructions

#### API Key

- [OpenAI](https://platform.openai.com/api-keys) API key (paid) or [Groq](https://console.groq.com/keys) API key (free)

## BeeAI Platform

### Prerequisites to get started with BeeAI Platform

- [Homebrew](https://brew.sh/) (for macOS or Linux)

    If you don't already have Homebrew installed, run the following command in your terminal and follow the instructions to update your shell environment:

    ```shell
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

- [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) (for Windows users)

    See [Windows WSL2 setup instructions](https://docs.beeai.dev/introduction/installation#windows-wsl2-setup-instructions)

- BeeAI Installation

    !!! note
        If using Windows, open WSL2 by right-clicking the Start menu, selecting a terminal (e.g., PowerShell or Windows Terminal), and typing the `wsl` command. From there, run all the following installation commands inside the WSL shell, not the Windows shell.

    Install BeeAI using Homebrew:

    ```shell
    brew install i-am-bee/beeai/beeai
    ```

### Workshop Specific Requirements

1. Start the BeeAI background service:

    ```shell
    beeai platform start
    ```

2. Configure your LLM provider for the BeeAI Platform

    !!! note
        You will need your OpenAI or Groq API key available

    ```shell
    beeai env setup
    ```

3. In a separate terminal, get the workshop code:

    Option A: Clone with Git (Recommended):

    ```shell
    git clone https://github.com/IBM/beeai-workshop.git
    ```

    Option B: Download ZIP:
    If you're not comfortable with Git, [download the ZIP file](https://github.com/IBM/beeai-workshop/archive/refs/heads/main.zip) and extract it to your desired location.

4. Navigate to the workshop folder and open in VS Code:

    ```shell
    cd beeai-workshop/intro_acp_beeai
    code .
    ```

    !!! important
        Make sure to open the specific `intro_acp_beeai` folder in VS Code, not the entire `beeai-workshop` directory. This ensures proper project structure and dependencies.

    **Alternative:** You can also open VS Code first, then use "File > Open Folder" to navigate to and select the `beeai-workshop/intro_acp_beeai` folder.

5. Create a .env file based on the env.template file at the intro_acp_beeai directory level. Uncomment out either the OpenAI API Key or the Groq API key and add your own api.

    ```shell
    cp env.template .env
    ```

    !!! note
        For OpenAI you just need the API Key, for Groq you need to uncomment all 3 environment variables but only need to modify the API Key.

### Already have BeeAI installed? Update and restart it

```shell
brew services stop
brew uninstall arize-phoenix
brew upgrade beeai
beeai platform start --set phoenix.enabled=true
```