import os

import discord
import utils
from discord.ext import commands
from dotenv import load_dotenv
from openai import AsyncOpenAI

SYSTEM_PROMPT_CHAT = """You are a helpful, friendly, and knowledgeable assistant on Discord. Your goal is to assist users with a wide range of tasks and inquiries, from answering questions and providing information to facilitating conversations and managing tasks within the server."""

load_dotenv()

# Access the variables
api_key_deepseek = os.getenv("API_KEY_DEEPSEEK")
discord_token = os.getenv("DISCORD_BOT_TOKEN")


client = AsyncOpenAI(
    api_key=api_key_deepseek,
    base_url="https://api.deepseek.com",
)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# Global list to store thread IDs
created_threads = []

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")
    # Sync the commands with Discord
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s) with Discord.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.tree.command(name="chat", description="Create a discussion in a discord")
async def chat_public(interaction: discord.Interaction) -> None:
    try:
        # # Create a thread from the message
        thread = await interaction.channel.create_thread(
            name="Discussion", auto_archive_duration=60, type=discord.ChannelType.public_thread
        )
        await thread.send("Hello, how can I help you ? You can close this discussion by typing 'quit'")
        created_threads.append(thread.id)
        await interaction.response.send_message(f"New discussion created : {thread.mention}", ephemeral=True)

    except Exception as e:
        print(f"Error creating public thread: {e}")


@bot.event
async def on_message(message: discord.Message) -> None:
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message is in one of the tracked threads
    if isinstance(message.channel, discord.Thread) and message.channel.id in created_threads:
        if message.content.lower() == "quit":
            # Close the thread
            await message.channel.edit(archived=True, locked=False)
            await message.channel.send("Discussion closed. Bye !")
            # Remove the thread ID from the list
            created_threads.remove(message.channel.id)
            return

        async with message.channel.typing():
            prompt = await utils.create_history(message, SYSTEM_PROMPT_CHAT)
            answer = await utils.get_chat_completion(client, prompt)
            await message.channel.send(answer)


bot.run(discord_token)
