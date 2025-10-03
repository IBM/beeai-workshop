# Intro to BeeAI Framework

Temporary notes for stuff here. We'll use the workshop web pages for most instructions, but this is a quick and handy way to describe what is here.

## Overview

This is the source for the workshop.
Put links to docs here.

## Files

* ipynb is for running workshop in colab or Jupyter environments

## Setup

* Ollama/granite

* For the colab/jupyter setup:
    * Colab is easy see the doc page
    * TODO: jupyter install notes here for running locally

### Demo BeeAI Platform

* `src/*` is for running the agent locally

#### Pre-work

1. install uv
2. install ollama
3. `ollama pull granite 3.3`

#### Install BeeAI Platform

* BeeAI Platform install, setup, start
    * `beeai platform start --set phoenix.enabled=true`
    * `beeai ui`
      * Select provider: Ollama
      * Select model: Granite 3.3
    * The BeeAI Platform user interfaces opens in your browser with the out-of-the-box agents

#### Create and serve Conference Prep agent

1. `git clone https://github.com/IBM/beeai-workshop.git`
2. `cd beeai-workshop/intro_beeai_platform`
3. `cp env.template .env`  # Note: The defaults are for ollama/granite3.3
4. `uv python install 3.13`
5. `uv sync`
6. `uv run src/agent.py`
   * Automatically registers with BeeAI Platform
   * Go back to your browser to see the Conference Prep Agent added

#### Running the Conference Prep Agent

* Run the agent locally with BeeAI Platform (todo can make sure it also works w/o platform?)
    * Install uv
    * Navigate to the repo/project directory (beeai_workshop/intro_beeai_framework)
    * Use uv to install the required version of python:
        * `uv python install 3.13`
    * `uv sync`
    * Set your IDE python interpreter to the one in .venv/bin/python (relative to this project directory)
    * Create a .env file from the template
        * `cp env.template .env`
    * Edit the .env file (defaults using local ollama should just work)
    * Run the agent:
       * `uv run src/agent.py` -- serves the agent self-registering with BeeAI platform

#### Running the Conference Prep Agent

Example input:

* I'm planning on meeting the Moderna rep at the next conference. Give me a one pager and remind me where we left off on previous discussions.
* More TBD

Notes:

* Selecting `detailed` is probably more likely to show sources
* Selecting `list` is nice for showing the widget worked

#### Looking at what OpenTelemetry captured

  * `http://localhost:6006/`
  * open project "default"
  * Select "All" (not Root Spans)
  * Most details show up after the run
  * TODO: Some examples of what to look for

#### Looking at the code

  * Setup IDE to use the project venv/bin/python3.13
  * Look for:
    * How the agent became a BeeAI Platform/A2A agent (using @server.agent)
    * How form was created and used
    * How instrumentation was added (OpenTelemetry for Arize Phoenix)
    * The RequirementAgent details (same as the intro_beeai_framework)
      * Revisit tools
      * Revisit requirement conditions
    * How source citations are added
