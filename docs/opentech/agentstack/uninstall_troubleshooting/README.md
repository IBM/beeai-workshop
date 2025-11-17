---
title: Uninstall and Troubleshooting
description: How to uninstall Agent Stack and troubleshoot common issues
logo: images/ibm-blue-background.png
---

# Uninstall and Troubleshooting

## Uninstalling Agent Stack

### Complete Uninstall

To completely remove Agent Stack from your system, follow the "Uninstall" section in the [Agent Stack documentation installation guide](https://docs.beeai.dev/introduction/installation#uninstall) depending on how you installed Agent Stack.

## Getting Help

### CLI Documentation

You can access comprehensive CLI documentation directly from your terminal:

- View all available commands:

    ```shell
    agentstack --help
    ```

- Get help for specific commands:

    ```shell
    agentstack platform --help
    agentstack env --help
    agentstack ui --help
    ```

## Common Issues and Solutions

### Port Conflicts

**Problem:** "Port already in use" error when starting agents

**Solution:**

1. Check what's running on the port:

    ```shell
    lsof -i :<PORT>
    ```

2. Kill the process if needed, substituting the number in the "PID" column:

    ```shell
    kill -9 <PID>
    ```

3. Or use a different port (configured in `.env` file)

### Agent Stack Won't Start

**Problem:** `agentstack platform start` fails

**Solutions:**

1. Try stopping and restarting:

    ```shell
    agentstack platform delete
    agentstack platform start
    ```

### API Key Issues

**Problem:** Authentication errors or "Invalid API key"

**Solutions:**

1. Reconfigure your LLM provider:

    ```shell
    agentstack env setup
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

**Problem:** Agent Stack UI doesn't load in browser

**Solutions:**

1. Upgrade Agent Stack to the latest version
2. Run this command, which will check the platform and env:

    ```shell
    agentstack ui
    ```

3. Recreate your Agent Stack platform instance and try again:

    ```shell
    agentstack platform delete
    agentstack platform start
    agentstack ui
    ```

### Workshop Files Missing

**Problem:** Can't find workshop files or folders

**Solutions:**

1. Ensure you cloned the correct repository:

    ```shell
    git clone https://github.com/IBM/beeai-workshop.git
    ```

2. Navigate to the correct directory:

    ```shell
    cd beeai-workshop/agentstack
    ```

3. Verify the files exist:

    ```shell
    ls -la src/
    ```

## Reset and Clean Installation

If you're experiencing persistent issues, try a clean reinstall -- follow the "Uninstall" section and then the "Install" section in the [BeeAI installation documentation](https://docs.beeai.dev/introduction/installation).

## Getting Additional Support

If you continue to experience issues:

1. Check the [Agent Stack documentation](https://docs.beeai.dev)
2. Review the [GitHub repository](https://github.com/IBM/beeai-workshop) for known issues
3. Ensure all prerequisites from the pre-work section are met

!!! tip
    When reporting issues, include the output of `agentstack --version` and your operating system information to help with troubleshooting.
