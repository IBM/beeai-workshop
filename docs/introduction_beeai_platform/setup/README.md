---
title: Setup Instructions
description: Setup the repo and environment
logo: images/BeeAI-Logo-White.png
---

# Workshop Setup Instructions

## Get the Workshop Code

**Option A: Clone with Git (Recommended):**

```bash
git clone https://github.com/IBM/beeai-workshop.git
```

**Option B: Download ZIP:**

If you're not comfortable with Git, [download the ZIP](https://github.com/IBM/beeai-workshop/archive/refs/heads/main.zip) file and extract it to your desired location.

---

## Open the Workshop in VS Code

Navigate to the specific workshop folder and open it in VS Code:

```bash
cd beeai-workshop/intro_beeai_platform
code .
```

**Important:**  
Make sure to open the specific `intro_beeai_platform` folder in VS Code, not the entire `beeai-workshop` directory.  
This ensures proper project structure and dependencies are detected.

Alternatively, you can open VS Code first and use `File > Open Folder` to navigate to and select the correct folder.

---

## Set Up Environment Variables

Create a `.env` file based on the existing `env.template` at the `intro_beeai_platform` directory level.  

```bash
cp env.template .env
```

In your new .env file:

1. Review the settings
2. Optionally, add your **OpenAI** key

---

## Install Project Dependencies

1. **Use uv to install the required version of python:**

    ```bash
    uv python install 3.13
    ```

2. **Install all required dependencies:**

    ```bash
    uv sync
    ```

This ensures you have the correct versions of all packages used in the workshop, installed in the correct environment.
