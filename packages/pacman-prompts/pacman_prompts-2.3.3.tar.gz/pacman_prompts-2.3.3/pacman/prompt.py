# defines an llm prompt class
import os
from pacman.models import *

FALLBACK_MODEL = "gpt-4o-mini"

class PromptConfig:
    def __init__(self, config):
        # set attributes from config
        for name, value in config.items():
            setattr(self, name, value)


class Prompt:
    def __init__(self, prompts, provider, config, name):
        self.config = PromptConfig(config)

        self.provider = provider

        self.name = name

        if type(prompts) == str:
            self.user_prompt = prompts
            return

        if "system" not in prompts and "user" not in prompts:
            raise Exception("Prompt must have either system prompt or user prompt")
        if "system" in prompts:
            self.system_prompt = prompts["system"]
        if "user" in prompts:
            self.user_prompt = prompts["user"]

    def compile(self, inputs):
        print(**inputs)
        return self.prompt.format(**inputs)

    def run(self, system_inputs=None, user_inputs=None, **kwargs):
        # format string
        complete_prompt = self.compile(user_inputs)
        if kwargs.get("debug", True):
            print(complete_prompt)
        # run in language model
        res = openai_client.completions.create(
            prompt=complete_prompt,
            **self.config.__dict__,
            # stop='\n'
        )
        return res
        # return output

    def __call__(self, *args, system_inputs=None, user_inputs=None, **kwargs):
        if len(args) == 0:
            return self.run(
                system_inputs=system_inputs, user_inputs=user_inputs, **kwargs
            )

        if len(args) == 1:
            return self.run(user_inputs=args[0], **kwargs)

        raise ValueError("Invalid number of arguments for __call__ method.")

    def log_call(self, model_name, prompt, response, response_model=None):
        with logfire.span(f'{model_name} {self.name} call') as span:
            logfire.info('Model call information')
            span.set_attribute('model_name', model_name)
            span.set_attribute('prompt', prompt)
            span.set_attribute('response', response)
            span.set_attribute('response model', response_model)

def load_prompt(loaded_file):
    prompt = Prompt(**loaded_file)


# make copy of Prompt class but use ChatCompletion in run method
class ChatPrompt(Prompt):
    def format_messages(self, system_inputs=None, user_inputs=None, **kwargs):
        if hasattr(self, "system_prompt"):
            system_prompt = self.system_prompt.format(**system_inputs)
        if hasattr(self, "user_prompt"):
            user_prompt = self.user_prompt.format(**user_inputs)

        initial_message_list = []

        if hasattr(self, "system_prompt"):
            initial_message_list.append({"role": "system", "content": system_prompt})
        if (
            kwargs.get("few_shot", False)
            and hasattr(self, "system_prompt")
            and hasattr(self, "user_prompt")
        ):
            initial_message_list.extend(kwargs.get("messages", []))
        if hasattr(self, "user_prompt"):
            initial_message_list.append({"role": "user", "content": user_prompt})

        if kwargs.get("messages", None) and not kwargs.get("few_shot", False):
            messages = initial_message_list + kwargs["messages"]
        else:
            messages = initial_message_list

        return messages

    def run(self, system_inputs=None, user_inputs=None, response_format=None, **kwargs):
        messages = self.format_messages(
            system_inputs=system_inputs, user_inputs=user_inputs, **kwargs
        )

        if kwargs.get("debug", True):
            print("complete prompt:")
            print(messages)

        if self.provider == Provider.OPENAI.value:
            if response_format:
                res = openai_client.beta.chat.completions.parse(
                    messages=messages,
                    response_format=response_format,
                    **self.config.__dict__,
                )
            else:
                res = openai_client.chat.completions.create(
                    messages=messages,
                    **self.config.__dict__,
                )
        elif self.provider == Provider.ANTHROPIC.value:
            if messages and messages[0]["role"] == "system":
                msgs = []
                if len(messages) > 1:
                    msgs = messages[1:]
                system_content = messages[0]["content"]
                res = anthropic_client.messages.create(
                    system=system_content, messages=msgs, **self.config.__dict__
                )
            else:
                res = anthropic_client.messages.create(
                    messages=messages, **self.config.__dict__
                )
        elif self.provider == Provider.ANYSCALE.value:
            try:
                res = anyscale_client.chat.completions.create(
                    messages=messages, **self.config.__dict__
                )
                self.log_call(self.config.model, messages, res)
            except Exception as e:
                print("Anyscale failed, fallback to OpenAI", e)
                self.config.model = FALLBACK_MODEL  # Set fallback model
                res = openai_client.chat.completions.create(
                    messages=messages, **self.config.__dict__
                )

        elif self.provider == Provider.FIREWORKS.value:
            try:
                res = fireworks_client.chat.completions.create(
                    messages=messages, **self.config.__dict__
                )
            except Exception as e:
                print("Fireworks failed, fallback to OpenAI", e)
                self.config.model = FALLBACK_MODEL  # Set fallback model
                res = openai_client.chat.completions.create(
                    messages=messages, **self.config.__dict__
                )
            # self.log_call(self.config.model, messages, res)

        elif self.provider == Provider.GROQ.value:
            try:
                res = groq_client.chat.completions.create(
                    messages=messages,
                    **self.config.__dict__,
                    # stop='\n'
                )
                self.log_call(self.config.model, messages, res)
            except Exception as e:
                print("Groq rate limit, fallback to openai", e)
                # Use the model map for fallback to anyscale
                self.config.model = FALLBACK_MODEL  # Set fallback model
                res = openai_client.chat.completions.create(
                    messages=messages, **self.config.__dict__
                )
        return res


class InstuctorPrompt(ChatPrompt):
    def run(self, system_inputs=None, user_inputs=None, response_model=None, response_format=None, **kwargs):
        messages = self.format_messages(
            system_inputs=system_inputs, user_inputs=user_inputs, **kwargs
        )

        if kwargs.get("debug", True):
            print("complete prompt:")
            print(messages)

        if self.provider == Provider.OPENAI.value:
            if response_format:
                print("using beta structured responses")
                res = instructor_openai_client.beta.chat.completions.parse(
                    messages=messages,
                    response_format=response_format,
                    **self.config.__dict__,
                )
            else:
                res = instructor_openai_client.chat.completions.create(
                    messages=messages, response_model=response_model, **self.config.__dict__
                )

        if self.provider == Provider.ANTHROPIC.value:
            res = instructor_anthropic_client.messages.create(
                messages=messages, response_model=response_model, **self.config.__dict__
            )

        if self.provider == Provider.ANYSCALE.value:
            try:
                res = instructor_anyscale_client.chat.completions.create(
                    messages=messages, response_model=response_model, **self.config.__dict__
                )
                self.log_call(self.config.model, messages, res, response_model)
            except Exception as e:
                print("Anyscale failed, fallback to OpenAI", e)
                self.config.model = FALLBACK_MODEL  # Set fallback model
                res = instructor_openai_client.chat.completions.create(
                    messages=messages, response_model=response_model, **self.config.__dict__
                )

        if self.provider == Provider.FIREWORKS.value:
            try:
                res = instructor_fireworks_client.chat.completions.create(
                    messages=messages, response_model=response_model, **self.config.__dict__
                )
                # self.log_call(self.config.model, messages, res, response_model)
            except Exception as e:
                print("Fireworks failed, fallback to OpenAI", e)
                self.config.model = FALLBACK_MODEL  # Set fallback model
                res = instructor_openai_client.chat.completions.create(
                    messages=messages, response_model=response_model, **self.config.__dict__
                )
                # self.log_call(self.config.model, messages, res, response_model)

        if self.provider == Provider.GROQ.value:
            try:
                res = instructor_groq_client.messages.create(
                    messages=messages, response_model=response_model, **self.config.__dict__
                )
                self.log_call(self.config.model, messages, res, response_model)
            except Exception as e:
                print("Groq rate limit, fallback openai", e)
                self.config.model = FALLBACK_MODEL  # Set fallback model
                res = instructor_openai_client.chat.completions.create(
                    messages=messages, response_model=response_model, **self.config.__dict__
                )
        return res


    def __call__(
        self, *args, system_inputs=None, user_inputs=None, response_model=None, **kwargs
    ):
        if len(args) == 0:
            return self.run(
                system_inputs=system_inputs,
                user_inputs=user_inputs,
                response_model=response_model,
                **kwargs,
            )

        if len(args) == 1:
            return self.run(user_inputs=args[0], **kwargs)

        raise ValueError("Invalid number of arguments for __call__ method.")
