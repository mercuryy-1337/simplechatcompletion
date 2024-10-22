import json
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Init openai client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def save_conversation(conversation):
    """Saves the conversation to a local JSON file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"conversation_{timestamp}.json"
    try:
        with open(filename, "w") as f:
            json.dump(conversation, f, indent=4)
        print(f"Conversation saved to {filename}")
    except Exception as e:
        print(f"Error saving conversation: {str(e)}")


class Chatbot:
    """Encapsulates the chat functionality with GPT-4."""

    def __init__(self, client):
        self.client = client
        self.conversation = []

    def chat_with_gpt(self, message):
        """Simple interactive chat with GPT-4."""
        print("Welcome to the GPT-4 Chat Interface! Type 'exit' to quit.\n")
        for message in self.conversation:
            print(f"{message['role']}: {message['content']}")
        while True:
            user_message = message
            
            # if user_message.lower() == "exit":
            #     print("Chat session ended. Goodbye!")
            #     save_conversation(self.conversation)
            #     break

            self.conversation.append({"role": "user", "content": user_message})

            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a very helpful assistant."},
                        {"role": "user", "content": user_message}
                    ]
                )
                assistant_reply = response.choices[0].message.content
                assistant_reply = {"Assistant": assistant_reply}
                self.conversation.append({"role": "assistant", "content": assistant_reply})
                
                return assistant_reply

            except Exception as e:
                print(f"Error: {str(e)}")
                return {"error": str(e)}

    def check_engine_type(self):
        """Asks GPT-4 a specific question about car engines."""
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", 
                     "content": "You are a helpful assistant."},
                    {"role": "user", 
                     "content": "What is the engine for the first generation BMW M2?"}
                ]
            )
            print(completion.choices[0].message.content)
        except Exception as e:
            print(f"Error: {str(e)}")


class Assistant:
    """Encapsulates the assistant logic and separates it from other functions."""

    def __init__(self):
        self.conversation = []
        self.vector_store = client.beta.vector_stores.create(name="Programming documents")
        self.file_paths = ['test.py']
        self.file_streams = [open(file_path, "rb") for file_path in self.file_paths]

    def assist_me(self, message):
        """Interactive assistant with enhanced capabilities."""
        while True:
            user_message = message

            # if user_message.lower() == "exit":
            #     print("Chat session ended. Goodbye!")
            #     save_conversation(self.conversation)
            #     break

            try:
                # Upload a file for the assistant to use
                file = client.files.create(file=open("test.py", "rb"), purpose="assistants")
                # Create a new assistant with tools enabled
                assistant = client.beta.assistants.create(
                    name="Programming Assistant",
                    instructions=(
                        "You are a personal programming lecturer. "
                        "You can help with Python, JavaScript, and TypeScript, "
                        "and are well-versed in CI/CD pipelines."
                    ),
                    tools=[{"type": "code_interpreter"}],
                    tool_resources={"code_interpreter": {"file_ids": [file.id]}},
                    model="gpt-4o",
                )

                # Start a new thread for the conversation
                thread = client.beta.threads.create()
                client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=user_message,
                    attachments=[{"file_id": file.id, "tools": [{"type": "code_interpreter"}]}]
                )

                # Run and poll the assistant
                run = client.beta.threads.runs.create_and_poll(
                    thread_id=thread.id, assistant_id=assistant.id, model="gpt-4o"
                )

                if run.status == 'completed':
                    messages = client.beta.threads.messages.list(thread_id=thread.id)
                    for message in messages:
                        if message.role == "assistant":
                            print(f"{message.role}: {message.content[0].text.value}")
                else:
                    print(f"Error: Assistant run failed. Status: {run.status}")
                    break

            except Exception as e:
                print(f"Error: {str(e)}")
                break


if __name__ == "__main__":
    assistant = Assistant()
    chatbot = Chatbot(client=client)
    # assistant.assist_me("What engine is used for the first generation BMW M2?")
    print(chatbot.chat_with_gpt("What engine is used for the first generation BMW M2?"))