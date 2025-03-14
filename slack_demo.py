import asyncio
import os

from agents import Agent, Runner
from arcade_slack.tools.chat import send_dm_to_user

from wrappers import arcade_tool_wrapper


SLACK_USER_ID = os.getenv("SLACK_USER_ID")


async def main():
    slack_agent = Agent(
        name="Slack agent",
        instructions="You are a helpful assistant that can assist with Slack messages, channels, and users.",
        model="gpt-4o-mini",
        tools=[arcade_tool_wrapper(send_dm_to_user, "arcade_slack")],
    )

    username = input("Send a DM to the username: ")
    message = input("Message: ")

    result = await Runner.run(
        starting_agent=slack_agent,
        input=f"Send a DM to the user '{username}' saying '{message}'",
        context={"user_id": SLACK_USER_ID},
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
