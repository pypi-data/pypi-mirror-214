import logging, json
from .util import read_source_files_until_marker, get_code

MARKER = "@dev"  # !@dev
NOT_MARKER = f"!{MARKER}"

ONE_SHOT_INPUT_CODE = '''
# Python source file name: utils.py
def validate_https_scheme_and_domain(url: str) -> bool:
    """
    Checks if the given string is a URL comprised of a well-formed scheme and
    network location. Uses both regex pattern matching and the urlparse function
    from urllib.parse python module. Raises ValueError for missmatched inputs.
    """
    import re, urllib.parse

    pattern = "^https:\/\/[0-9A-z.\-]+.[0-9A-z.\-]+.[a-z]+$"
    result = re.match(pattern, url)
    if not result:
        raise ValueError(f"Invalid url: {url}")

    result = urllib.parse(url)
    if not result.scheme or not result.netloc:
        raise ValueError(f"Invalid url: {url}")

    return True
'''

ONE_SHOT_OUTPUT_CODE = '''
# Python source file name: utils.py
def validate_https_scheme_and_domain(url: str) -> bool:
    """
    Checks if the given string is a URL comprised of a well-formed scheme and
    network location. Uses both regex pattern matching and the urlparse function
    from urllib.parse python module. Raises ValueError for missmatched inputs.
    """
    import re, urllib.parse

    pattern = "^https:\/\/[0-9A-z.\-]+.[0-9A-z.\-]+.[a-z]+$"
    result = re.match(pattern, url)
    if not result:
        raise ValueError(f"Invalid url: {url}")

    result = urllib.parse.urlparse(url)
    if not result.scheme or not result.netloc:
        raise ValueError(f"Invalid url: {url}")

    return True
'''

ONE_SHOT_OUTPUT = {
    "code": ONE_SHOT_OUTPUT_CODE,
    "findings": [
        {
            "message": "The `urllib.parse` function call has a typo. It should be `urllib.parse.urlparse(url)` instead of `urllib.parse(url)`."
        },
    ],
}

USER_REQUEST1 = (
    "Generate high quality python3 code that implements the requirements "
    "written in the docstring of the last function. Analyse the code for "
    "bugs and security issues, list the findings and if any, generate "
    "code that fixes these issues. Format your response as json and only "
    "return the json. Include your analysis as fields in the json response."
)

USER_REQUEST = (
    "Generate high quality python3 code that implements the requirements "
    "written in the docstring of the last function. Format your response as "
    "json and only return the json. Include your analysis as fields in the "
    "json response."
)


class FunctionGenerator:
    def __init__(self, prompt):
        self._prompt = prompt

    def generate(self, *file_names):
        source_code = read_source_files_until_marker(*file_names, marker=MARKER, not_marker=NOT_MARKER)

        logging.debug(f"Generating function...")
        result = self._prompt(
            source_code,
            USER_REQUEST,
            {
                "source_code": ONE_SHOT_INPUT_CODE,
                "user_request": USER_REQUEST,
                "assistant_answer": json.dumps(ONE_SHOT_OUTPUT),
            },
        )
        return get_code(result, "code")
