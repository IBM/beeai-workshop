---
title: Kitchen-Aide Agent Showcasing Conditional Requirements
description: Exploring Conditional Requirements with a fun kitchen
  example
logo: images/BeeAI-Logo-White.png
---

# Kitchen-Aide Agent: Conditional Requirements 🍳🐝

In this notebook, you'll learn how **Conditional Requirements** shape
what tools an agent *can see and use* on each turn. Using a playful
**Kitchen-Aide Agent**, you'll explore how developer-defined rules can
restrict, allow, or sequence tool access.

<hr>

## 🥘 Workshop Scenario

Your Kitchen-Aide Agent helps you make cooking decisions using:

- Your **fridge**, **freezer**, and **pantry** inventory tools
- Your **personal recipe search**
- An optional **internet recipe tool**

You'll ask questions like:

- "What can I make with what I already have?"
- "What ingredients am I missing for this recipe?"
- "Is there a web recipe that fits my ingredients?"

The key lesson: **conditional requirements decide which of these tools
the LLM is even allowed to call on each turn.**

<hr>

## 📚 What You'll Learn

### ⭐ Conditional Requirements

You'll implement rules such as:

- A tool can be used only once (e.g., `get_fridge`)\
- Certain tools are hidden until another tool has been used\
- A tool may require a specific argument before the LLM can call it\
- A tool may be temporarily unavailable depending on state

These rules can either force a workflow or simply **expose or hide
tools** based on developer-defined conditions.

<hr>

## 🚀 Getting Started

**Quick Setup**
    - Google Account – Required for accessing Google Colab
    - Workshop Notebook – Open the notebook <a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/IBM/beeai-workshop/blob/main/kitchen-aide/beeai_kitchen_aide.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
    - Personal Copy – If you'd like to save your changes, please copy this notebook and create your own version

Then:

- Configure your agent and tools
- Add Conditional Requirements
- Test how the agent's accessible tools change as you interact

<hr>

## Learn More About BeeAI

- 📚 **Framework Documentation**: [https://framework.beeai.dev/introduction/welcome](https://framework.beeai.dev/introduction/welcome)
- 🧠 **GitHub Repository**: [https://github.com/i-am-bee/beeai-framework](https://github.com/i-am-bee/beeai-framework)