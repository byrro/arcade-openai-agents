import asyncio

import arcade_slack
from agents import Agent, Runner

from wrappers import arcade_tool_wrapper


SLACK_USER_ID = "U086XD0GGCW"


async def main():
    slack_agent = Agent(
        name="Slack agent",
        instructions="You are a helpful assistant that can assist with Slack messages, channels, and users.",
        model="gpt-4o-mini",
        tools=[arcade_tool_wrapper(arcade_slack.tools.chat.send_dm_to_user, "arcade_slack")],
    )
    result = await Runner.run(
        starting_agent=slack_agent,
        input="Send a DM to the user 'sam' saying 'Hello, from OpenAI Agents SDK!'",
        context={"user_id": SLACK_USER_ID},
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
