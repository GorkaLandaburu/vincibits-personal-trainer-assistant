import openai
from dotenv import find_dotenv, load_dotenv
import os
import time
import logging
from datetime import datetime


# Initialize OpenAI client
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
model = "gpt-3.5-turbo-16k"

def create_assistant(client, model):
    """Create an assistant."""
    personal_trainer_assis = client.beta.assistants.create(
        name="Personal Trainer",
        instructions="""You are the best personal trainer and nutritionist who knows how to get clients to build lean muscles.\n
         You've trained high-caliber athletes and movie stars. """,
        model=model,
    )
    return personal_trainer_assis.id

def create_thread(client):
    """Create a thread."""
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "How do I get started working out to lose fat and build muscles?",
            }
        ]
    )
    return thread.id

def create_message(client, thread_id, message):
    """Create a message in the thread."""
    return client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=message
    )

def run_assistant(client, thread_id, assistant_id):
    """Run the assistant."""
    return client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Please address the user as James Bond",
    )

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """Wait for a run to complete and print the elapsed time."""
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

def main():
    # Hardcoded IDs
    assistant_id = "asst_7yT5g1MShqrN1534vDrqm810"
    thread_id = "thread_kr871DUEaGcTXkBb2jHO9eJ6"

    # Create a message
    message_content = "How many reps do I need to do to build lean muscles?"
    create_message(client, thread_id, message_content)

    # Run the assistant
    run = run_assistant(client, thread_id, assistant_id)

    # Wait for the run to complete
    wait_for_run_completion(client, thread_id, run.id)

    # Log the steps
    run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
    print(f"Steps---> {run_steps.data[0]}")

if __name__ == "__main__":
    main()