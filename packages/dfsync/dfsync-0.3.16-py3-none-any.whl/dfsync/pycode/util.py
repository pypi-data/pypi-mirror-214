import json, logging
from pprint import pprint


def read_source_files(*file_names):
    sources = []
    for name in file_names:
        logging.debug(f"Reading {name}")
        with open(name) as f:
            content = f.read()
            file_source = f"# Python source file name: {name}\n\n{content.strip()}"
            sources.append(file_source)
    logging.debug(f"Done reading {len(sources)} files")
    return "\n".join(sources)


def read_source_files_until_marker(*file_names, marker=None, not_marker=None):
    source_code = read_source_files(*file_names)
    if not marker or not not_marker:
        return source_code

    source_context = []
    for line in source_code.split("\n"):
        if marker in line and not_marker not in line:
            break
        source_context.append(line)
    return "\n".join(source_context)


def get_code_from_markdown(markdown_message: str) -> str:
    """
    Returns the contents of the first code block from the given body of markdown
    text. Works correctly with code blocks that contains the markdown triple-backticks.

    :param markdown_message: str - a string containing markdown text, including code blocks
    :return: str - the contents of the first code block in the markdown text
    """

    # Split the markdown message by triple backticks to get all code blocks
    code_blocks = markdown_message.split("```")
    if len(code_blocks) > 3:
        print(markdown_message)
        raise ValueError("Found multiple code blocks, expecting only one")
    elif len(code_blocks) > 1:
        print(markdown_message)
        raise ValueError("Found corrupted markdown code block")
    else:
        print(markdown_message)
        raise ValueError("No code block found in markdown")

    block = code_blocks[1].strip()
    language = "python"
    if block.startswith(language):
        block = block[len(language) :].strip()

    return block


def get_code(content: str, key: str = "code") -> str:
    """
    Get the code part of a json object or the content of its first markdown code block.
    If a json object is passed, the function will try to parse it based on the json module and
    return the value associated with the 'code' key.
    If this approach fails, the function will treat the object as markdown text and
    extract the contents of the first code block that makes use of the triple-backtick notation.

    If the passed argument does not provide any usable content, an error will be thrown as a ValueError.

    :param content: str - a string that contains either a json object or markdown text
    :param key: str - if a json object is parsed, the key to its value that is the code that will be returned

    :return: str - the code found in the given object, or an Exception if any errors occur
    """
    if not content:
        raise ValueError("Can't get code, received empty content")
    try:
        parsed = json.loads(content)
    except ValueError:
        return get_code_from_markdown(content)

    try:
        if "findings" in parsed:
            print("\n".join([f["message"] for f in parsed["findings"]]))

        return parsed[key]
    except:
        pprint(parsed)
        raise
