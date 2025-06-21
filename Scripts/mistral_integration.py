import asyncio
import os
from mistralai import Mistral

async def query_mistralai(prompt):
    # Access the environment variable named "MISTRAL_API_KEY"
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"
    client = Mistral(api_key=api_key)

    response = await client.chat.stream_async(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    async for chunk in response:
        if chunk.data.choices[0].delta.content is not None:
            print(chunk.data.choices[0].delta.content, end="")

if __name__ == "__main__":
    # Example usage
    prompt = "Briefly tell me how to find fire alerts in my area and provide essential safety advice."
    asyncio.run(query_mistralai(prompt))
