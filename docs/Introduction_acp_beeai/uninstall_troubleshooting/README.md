---
title: Uninstall and Troubleshooting
description: How to uninstall BeeAI and troubleshoot common issues
logo: images/ibm-blue-background.png
---

# Uninstall and Troubleshooting

## Uninstalling BeeAI

### Complete Uninstall

To completely remove BeeAI from your system:

1. Stop the BeeAI platform service:

    ```shell
    beeai platform stop
    ```

2. Uninstall BeeAI using Homebrew:

    ```shell
    brew uninstall beeai
    ```

### Uninstall Dependencies

If you also want to remove related dependencies that were installed:

```shell
brew uninstall arize-phoenix
```

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
2. Kill the process if needed:
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
    beeai platform stop
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
1. Ensure you're using Python >=3.11:
    ```shell
    python --version
    ```
2. Try clearing UV cache:
    ```shell
    uv cache clean
    ```
3. Reinstall dependencies:
    ```shell
    uv sync --reinstall
    ```

### Browser Issues

**Problem:** BeeAI UI doesn't load in browser

**Solutions:**
1. Try a different browser or incognito/private mode
2. Clear browser cache and cookies
3. Ensure the BeeAI platform is running:
    ```shell
    beeai platform start
    beeai ui
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
    cd beeai-workshop/intro_acp_beeai
    ```
3. Verify the files exist:
    ```shell
    ls -la src/
    ```

## Reset and Clean Installation

If you're experiencing persistent issues, try a clean reinstall:

1. **Complete cleanup:**
    ```shell
    beeai platform stop
    brew uninstall beeai
    brew uninstall arize-phoenix
    ```

2. **Fresh installation:**
    ```shell
    brew install i-am-bee/beeai/beeai
    beeai platform start
    beeai env setup
    ```

## Getting Additional Support

If you continue to experience issues:

1. Check the [BeeAI documentation](https://docs.beeai.dev)
2. Review the [GitHub repository](https://github.com/IBM/beeai-workshop) for known issues
3. Ensure all prerequisites from the pre-work section are met

!!! tip
    When reporting issues, include the output of `beeai --version` and your operating system information to help with troubleshooting.