# OpenAI Agents powered by Arcade Tools

This is a demo of using OpenAI Agents with Arcade Tools.

To run the demo:

1. Install the dependencies with `pip install -r requirements.txt`
1. Set the environment variables:
    - `SLACK_USER_ID` with your own Slack user ID.
    - `OPENAI_API_KEY` with your OpenAI API key.
    - `ARCADE_API_KEY` with your Arcade API key.
1. Execute `python slack_demo.py` (recommended Python 3.10+).

It will prompt you for a Slack username and a message, which will be sent to this user. The first time you run the demo, it will prompt you to authorize the Arcade Slack tool to send messages on your behalf.

You can register for an Arcade account at [https://arcade.dev](https://arcade.dev).

Obs.: to find your Slack user ID, go to Slack, open your profile, click on the 'three dots', and hit "Copy Member ID".
