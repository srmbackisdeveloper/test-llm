import asyncio
from app.db.queries import get_thread_id, save_thread_id
from app.settings import OPENAI_API_KEY, ASSISTANT_ID
from openai import OpenAI

async def get_assistant_response(user_id, content):
    client = OpenAI(api_key=OPENAI_API_KEY)
    thread_id = get_thread_id(user_id)

    try:
        if not thread_id:
            print("CREATING NEW THREAD...\n")
            thread = await asyncio.to_thread(client.beta.threads.create)
            thread_id = thread.id
            save_thread_id(user_id, thread_id)

        await asyncio.to_thread(
            client.beta.threads.messages.create,
            thread_id=thread_id,
            role="user",
            content=content
        )

        run = await asyncio.to_thread(
            client.beta.threads.runs.create_and_poll,
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,
        )

        print(f"Run completed with status: {run.status}")

        if run.status == "completed":
            print("COMPLETED\n")
            messages = await asyncio.to_thread(client.beta.threads.messages.list, thread_id=thread_id)
            usage = run.usage # сколько токенов юзер потратил на запрос, это для аналитики

            return messages.data[0].content[0].text.value

        elif run.status == "requires_action":
            print("ACTION REQUIRED\n")
            return "done requires_action"

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        if 'run' in locals():
            await asyncio.to_thread(client.beta.threads.runs.cancel, run_id=run.id)
        return "Send again, something went wrong"
