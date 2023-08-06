import logging, os, openai

openai.api_key = os.getenv("OPENAI_API_KEY", "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")


def python_prompt(source_code, user_request, *examples):
    prompt_prefix = {"role": "user", "content": "Given the following python code, analyse all of it."}

    example_messages = []
    for example in examples:
        example_messages = [
            *example_messages,
            prompt_prefix,
            {"role": "user", "content": example["source_code"]},
            {"role": "user", "content": example["user_request"]},
            {"role": "assistant", "content": example["assistant_answer"]},
        ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant trained on lots of "
                "expert python code annotated with code design quality "
                "assessments written by Guido van Rossum, the creator of python "
                "and an expert at evaluating high level code quality and "
                "source code design.",
            },
            *example_messages,
            prompt_prefix,
            {"role": "user", "content": source_code},
            {"role": "user", "content": user_request},
        ],
    )
    first_choice = response["choices"][0]
    message = first_choice["message"]["content"]
    return message


def prompt(source_code, user_request, *examples):
    return python_prompt(source_code, user_request, *examples)
