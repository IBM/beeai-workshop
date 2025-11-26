---
title: BeeAI Middleware Demo
description: A quick guide to understanding and exploring BeeAI
  Middleware
logo: images/BeeAI-Logo-White.png
---

# BeeAI Middleware Demo ⚙️

This demo introduces **BeeAI Middleware**, showing how you can intercept, modify, validate, or route agent requests to safegaurd against prompt injection attacks, invisible text, and secrets detection.

<hr>

## 🔧 What This Demo Covers

BeeAI Middleware lets you plug custom logic into the agent emitted event. In
this notebook, you'll explore how to:

- Inspect or transform **inputs** before the LLM sees them
- Enforce **middleware checks** such as formatting, guardrails, or LLM as judge
- Log and analyze **intermediate agent decisions**
- Modify or filter **outputs** before they reach the user
- Combine multiple middleware layers to create richer behavior

Middleware helps you shape agent interactions *without defining tools or
imposing conditional requirements*. It simply provides hooks into the
request/response flow.

<hr>

## 🚀 Getting Started

- Google Account – Required for accessing Google Colab
- Workshop Notebook – Open the notebook <a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/IBM/beeai-workshop/blob/main/middleware/beeai_middleware.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
- Personal Copy – If you'd like to save your changes, please copy this notebook and create your own version

## Learn More About BeeAI

## Learn More About BeeAI

- 📚 **Framework Documentation**: [https://framework.beeai.dev/introduction/welcome](https://framework.beeai.dev/introduction/welcome)
- 🧠 **GitHub Repository**: [https://github.com/i-am-bee/beeai-framework](https://github.com/i-am-bee/beeai-framework)