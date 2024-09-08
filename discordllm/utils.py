import discord
import openai

SYSTEM_PROMPT_CHAT = """You are a helpful, friendly, and knowledgeable assistant on Discord. Your goal is to assist users with a wide range of tasks and inquiries, from answering questions and providing information to facilitating conversations and managing tasks within the server."""

async def create_history(message: discord.Message) -> list:
    prompt = [{"role": "system", "content": SYSTEM_PROMPT_CHAT}]
    async for msg in message.channel.history(limit=None, oldest_first=True):
        role = "assistant" if "GregGPT" in str(msg.author) else "user"
        prompt.append({"role": role, "content": msg.content})
    return prompt


async def get_chat_completion(client: openai.AsyncOpenAI, prompt: str) -> str:
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=prompt,
        temperature=1.0,
    )
    return response.choices[0].message.content
