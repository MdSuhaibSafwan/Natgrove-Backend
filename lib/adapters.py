import json
import os
import time
import requests
import base64
import openai
from uuid import uuid4
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from openai import OpenAI
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def get_image_as_base64(url):
    return base64.b64encode(requests.get(url).content)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class GPTAssistant(object):

    def __init__(self, user, thread_id=None, assistant_id=None):
        if not user.is_authenticated:
            raise ValueError("User UnAuthorized")

        api_key = os.environ.get("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        self.client = client
        self.user = user
        self.set_default_assistant()

    def set_default_assistant(self):
            self.assistant_id = os.environ.get("assistant_id")
            return self.assistant_id

    def set_default_thread(self, thread):
        self.thread_id = thread.id
        return thread

    def create_thread(self, user):
        try:
            thread = self.client.beta.threads.create()

        except openai.BadRequestError as e:
            raise ValueError(e)

        except openai.APIConnectionError as e:
            raise ValueError(e)

        self.set_default_thread(thread)
        return thread

    def add_message_to_thread(self, content, file=None):
        try:
            message = self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=content
            )
        except openai.BadRequestError as e:
            raise ValueError(e)

        except openai.RateLimitError as e:
            raise ValueError(e)

        except openai.APIConnectionError as e:
            raise ValueError(e)

        except openai.InternalServerError as e:
            raise ValueError(e)

        return message

    def run_thread(self):
        run = self.client.beta.threads.runs.create(
        thread_id=self.thread_id,
        assistant_id=self.assistant_id,
        instructions=f"Please address the user as {self.user}. The user has a premium account."
        )
        return run

    def check_run_status(self, run):
        try:
            run = self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=run.id
            )

        except openai.APIConnectionError as e:
            raise ValueError(e)

        return run

    def check_run(self, run):
        while True:
            run = self.check_run_status(run, self.thread_id)
            if run.status == "completed":
                print(f"Run is completed.")
                break

            elif run.status == "expired":
                print(f"Run is expired.")
                break

            elif run.status == "requires_action":
                print("Run requires Action.")
                self.manage_action_for_run(thread_id, run)

            else:
                print(f"OpenAI: Run is not yet completed. Waiting...{run.status} ")
                time.sleep(3)

        return run

    def send_message_with_image(self, user, content, image_url):
        self.user = user
        base64_image = encode_image(image_url)
        api_key = os.environ.get("OPENAI_API_KEY")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": content
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                }
                ]
            }
            ],
                "max_tokens": 300
            }

        r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        response = r.json()
        bot_response = response["choices"][0]["message"]["content"]

        message_obj = self.add_user_message_to_db(user, content)
        self.add_image(image_url, message_obj)
        self.add_gpt_message_to_db(message_obj, bot_response)
        return bot_response
