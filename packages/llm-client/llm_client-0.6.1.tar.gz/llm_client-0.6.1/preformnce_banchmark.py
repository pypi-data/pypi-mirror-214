import asyncio
import os

from langchain.llms import OpenAI  # Or any other model avilable on LangChain

os.environ["OPENAI_API_KEY"] = " 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"

llm = OpenAI(model_name="text-ada-001")


async def run_langchain():
    print(await llm.agenerate(["Tell me a joke"]))


asyncio.run(run_langchain())
