---
title: Overview
description: Workshop Goals and 
logo: images/BeeAI-Logo-White.png
---


# Workshop Overview: Company Analysis Agent with the BeeAI Framework

In this workshop, you’ll be using the **BeeAI Framework** in partnership with **Tavily** and **Redis** to build a company analysis agent that demonstrates modern AI techniques in an enterprise context. Each section **includes interactive coding activities** where you’ll fill in missing code and run the files to test your progress.

---

## What You’ll Build

You’ll create a company analysis agent with access to three key tools:

1. **Tavily MCP Tool** – A locally run Tavily server used to perform real-time web searches
2. **Redis Retriever** – Connects to a Redis vector store and retrieves relevant internal knowledge
3. **Thinking Tool** – A reasoning module that enables the agent to follow a ReAct (Reasoning + Acting) pattern with chain-of-thought reasoning  
   👉 Read more about this pattern here: [IBM: ReAct Agent](https://www.ibm.com/think/topics/react-agent)

> 🛑 **Disclaimer**:  
> This is a demo application. **McDonald’s** is used purely as a real-world example for showcasing search-based functionality.  
> This project is **not affiliated with or endorsed by McDonald’s Corporation.**

---

## Workshop Structure

To ensure a smooth experience, follow the steps in this order:

1. ✅ [Prework](../pre-work/README.md) – Install dependencies and gather API keys
2. 🔧 [Setup](../setup/README.md) – Get the code and environment ready
3. 🛠️ [Create Tools](../tools/README.md) – Build the Tavily and Redis RAG tools
4. 🤖 [Create the Agent](../agent/README.md) – Assemble and run your company analysis assistant

If you get stuck at any point, solutions are available in the `src/solutions` folder.
---

## Learn More About BeeAI

- 📚 **Framework Documentation**: [https://framework.beeai.dev/introduction/welcome](https://framework.beeai.dev/introduction/welcome)
- 🧠 **GitHub Repo**: [https://github.com/i-am-bee/beeai-framework](https://github.com/i-am-bee/beeai-framework)

Explore what else you can build with BeeAI, including tool-rich agents, dynamic workflows, conditional logic, and more.