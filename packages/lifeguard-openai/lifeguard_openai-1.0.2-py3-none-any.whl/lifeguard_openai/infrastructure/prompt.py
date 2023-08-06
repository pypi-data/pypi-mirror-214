import openai

from lifeguard_openai.settings import (
    LIFEGUARD_OPENAI_TOKEN,
    LIFEGUARD_OPENAI_MODEL,
    LIFEGUARD_OPENAI_TEMPERATURE,
    LIFEGUARD_OPENAI_TOP_P,
    LIFEGUARD_OPENAI_FREQUENCY_PENALTY,
    LIFEGUARD_OPENAI_PRESENCE_PENALTY,
    LIFEGUARD_OPENAI_MAX_TOKENS,
)

openai.api_key = LIFEGUARD_OPENAI_TOKEN


def execute_prompt(prompt, options=None):
    default_options = {
        "model": LIFEGUARD_OPENAI_MODEL,
        "temperature": LIFEGUARD_OPENAI_TEMPERATURE,
        "top_p": LIFEGUARD_OPENAI_TOP_P,
        "frequency_penalty": LIFEGUARD_OPENAI_FREQUENCY_PENALTY,
        "presence_penalty": LIFEGUARD_OPENAI_PRESENCE_PENALTY,
        "max_tokens": LIFEGUARD_OPENAI_MAX_TOKENS,
    }

    if not options:
        options = {}
    options["prompt"] = prompt

    default_options.update(options)

    response = openai.Completion.create(**default_options)

    if response.choices:
        return response.choices[0].text
    return ""
