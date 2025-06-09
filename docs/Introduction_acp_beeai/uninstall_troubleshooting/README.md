---
title: Uninstall and Troubleshooting
description: How to uninstall BeeAI and troubleshoot common issues
logo: images/ibm-blue-background.png
---

# Uninstall and Troubleshooting

## Uninstalling BeeAI

### Complete Uninstall

To completely remove BeeAI from your system, follow the "Uninstall" section in the [BeeAI documentation installation guide](https://docs.beeai.dev/introduction/installation#uninstall) depending on how you installed BeeAI.

## Getting Help

### CLI Documentation

You can access comprehensive CLI documentation directly from your terminal:

- View all available commands:

    ```shell
    beeai --help
    ```

- Get help for specific commands:

    ```shell
    beeai platform --help
    beeai env --help
    beeai ui --help
    ```

## Common Issues and Solutions

### Port Conflicts

**Problem:** "Port already in use" error when starting agents

**Solution:**

1. Check what's running on the port:

    ```shell
    lsof -i :8000
    ```

2. Kill the process if needed, substituting the number in the "PID" column:

    ```shell
    kill -9 <PID>
    ```

3. Or use a different port:

    ```shell
    uv run src/ticket_workflow_agent.py --port 8001
    ```

### BeeAI Platform Won't Start

**Problem:** `beeai platform start` fails

**Solutions:**

1. Try stopping and restarting:

    ```shell
    beeai platform delete
    beeai platform start
    ```

### API Key Issues

**Problem:** Authentication errors or "Invalid API key"

**Solutions:**

1. Reconfigure your LLM provider:

    ```shell
    beeai env setup
    ```

2. Verify your API key is correctly set in the environment
3. Check that your API key has sufficient credits/quota

### Python/UV Issues

**Problem:** `uv sync` fails or Python dependency errors

**Solutions:**

1. Try clearing `uv` cache:

    ```shell
    uv cache clean
    ```

2. Reinstall dependencies:

    ```shell
    uv sync --reinstall
    ```

### Browser Issues

**Problem:** BeeAI UI doesn't load in browser

**Solutions:**

1. Upgrade BeeAI to the latest version
2. Run this command, which will check the platform and env:

    ```shell
    beeai ui
    ```

3. Recreate your BeeAI platform instance and try again:

    ```shell
    beeai platform delete
    beeai platform start
    beeai ui
    ```

### Workshop Files Missing

**Problem:** Can't find workshop files or folders

**Solutions:**

1. Ensure you cloned the correct repository:

    ```shell
    git clone https://github.com/JanPokorny/beeai-workshop.git
    ```

2. Navigate to the correct directory:

    ```shell
    cd beeai-workshop/intro_acp_beeai
    ```

3. Verify the files exist:

    ```shell
    ls -la src/
    ```

## Reset and Clean Installation

If you're experiencing persistent issues, try a clean reinstall -- follow the "Uninstall" section and then the "Install" section in the [BeeAI installation documentation](https://docs.beeai.dev/introduction/installation).

## Getting Additional Support

If you continue to experience issues:

1. Check the [BeeAI documentation](https://docs.beeai.dev)
2. Review the [GitHub repository](https://github.com/JanPokorny/beeai-workshop) for known issues
3. Ensure all prerequisites from the pre-work section are met

!!! tip
    When reporting issues, include the output of `beeai --version` and your operating system information to help with troubleshooting.
