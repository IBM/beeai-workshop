---
title: Setup Instructions
description: Setup the repo and environment
logo: images/BeeAI-Logo-White.png
---

# Setup Instructions

## Get the Demo Code

**Option A: Clone with Git (Recommended):**

```bash
git clone https://github.com/IBM/beeai-workshop.git
```

**Option B: Download ZIP:**

If you're not comfortable with Git, [download the ZIP](https://github.com/IBM/beeai-workshop/archive/refs/heads/main.zip) file and extract it to your desired location.

---

## Navigate to the demo folder

Navigate to the specific demo folder:

```bash
cd beeai-workshop/opentech
```

**Important:**  
Make sure to open the specific `opentech` folder, not the entire `beeai-workshop` directory.  
This ensures proper project structure and dependencies are detected.

---

## Install Project Dependencies

1. **Install all required dependencies:**

    ```bash
    uv --directory agentstack sync
    ```

This ensures you have the correct versions of all packages used in the lab, installed in the correct environment.
