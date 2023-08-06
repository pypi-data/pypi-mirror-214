import logging, json
from .util import read_source_files_until_marker, get_code

MARKER = "@index"  # !@index
NOT_MARKER = f"!{MARKER}"

ONE_SHOT_INPUT_CODE = """
# Python source file name: utils.py
def validate_https_scheme_and_domain(url: str) -> bool:
    import re, urllib.parse

    pattern = "^https:\/\/[0-9A-z.\-]+.[0-9A-z.\-]+.[a-z]+$"
    result = re.match(pattern, url)
    if not result:
        raise ValueError(f"Invalid url: {url}")

    result = urllib.parse.urlparse(url)
    if not result.scheme or not result.netloc:
        raise ValueError(f"Invalid url: {url}")

    return True
"""

USER_REQUESTS = [
    "Generate a short and high quality docstring that explains what the last "
    "function does and how it should be invoked by callers. Format your "
    "response as json and only return the json. Include your analysis as "
    "fields in the json response.",
    #
    "Generate 9 search questions/queries a user might ask about the last "
    "function. The answers to these questions must be derived from the body "
    "of this last function. Format your response as json and only return the "
    "json. ",
    #
    "Generate 10 hashtags that adequetly describe what the last function does. "
    "Format your response as json and only return the json.",
]
ONE_SHOT_OUTPUT_KEYS = ["docstring", "questions_and_answers", "hashtags"]
ONE_SHOT_OUTPUTS = [
    {
        "docstring": """
Checks if the given string is a URL comprised of a well-formed scheme and
network location. Uses both regex pattern matching and the urlparse function
from urllib.parse python module.

:param url: str - the string that will be validated

:return: bool - true if the given argument is a valid URL
:raises: ValueError when the given argument is an invalid URL
""",
        "findings": [
            {
                "message": "The regex does not match all possible valid urls, some valid urls are incorrectly labeled as invalid."
            },
        ],
    },
    {
        "questions_and_answers": {
            "1": {
                "question": "What is the input parameter type of the validate_https_scheme_and_domain function?",
                "answer": "The input parameter type of the function is str.",
            },
            "2": {
                "question": "What python standard library modules are imported in the validate_https_scheme_and_domain function?",
                "answer": "The function imports the re and urllib.parse modules.",
            },
            "3": {
                "question": "What is the purpose of the regular expression pattern variable from validate_https_scheme_and_domain?",
                "answer": "The regular expression pattern variable is used to check if the input url string matches the https scheme and domain pattern.",
            },
            "4": {
                "question": "What happens if the input url string does not match the https scheme and domain pattern?",
                "answer": "If the input url string does not match the https scheme and domain pattern, a ValueError is raised with a message indicating that the url is invalid.",
            },
            "5": {
                "question": "What method is invoked on the parsed url object?",
                "answer": "The urlparse method is invoked on the parsed url object to obtain information about the url's scheme and network location.",
            },
            "6": {
                "question": "What happens if the parsed url object does not have a scheme or network location?",
                "answer": "If the parsed url object does not have a scheme or network location, a ValueError is raised with a message indicating that the url is invalid.",
            },
            "7": {
                "question": "What is the purpose of the validate_https_scheme_and_domain function?",
                "answer": "The purpose of the function is to validate that a given url string matches the https scheme and domain pattern and has a valid scheme and network location.",
            },
            "8": {
                "question": "What is the expected output of the validate_https_scheme_and_domain function if the input url matches the https scheme and domain pattern and has a valid scheme and network location?",
                "answer": "The expected output of the function if the input url matches the https scheme and domain pattern and has a valid scheme and network location is True",
            },
            "9": {
                "question": "Where is the validate_https_scheme_and_domain defined?",
                "answer": "The validate_https_scheme_and_domain is defined in utils.py",
            },
        }
    },
    {
        "hashtags": [
            "#Python",
            "#urlValidation",
            "#secureURL",
            "#HTTPS",
            "#domainValidation",
            "#RegExp",
            "#urllibParse",
            "#inputValidation",
            "#urlparse",
            "#ValueError",
        ]
    },
]


class SearchExpansionGenerator:
    def __init__(self, prompt):
        self._prompt = prompt

    def generate(self, *file_names):
        source_code = read_source_files_until_marker(*file_names, marker=MARKER, not_marker=NOT_MARKER)

        logging.debug(f"Generating index...")
        for request_index, request in enumerate(USER_REQUESTS):
            result = self._prompt(
                source_code,
                request,
                {
                    "source_code": ONE_SHOT_INPUT_CODE,
                    "user_request": request,
                    "assistant_answer": json.dumps(ONE_SHOT_OUTPUTS[request_index]),
                },
            )
            result = get_code(result, ONE_SHOT_OUTPUT_KEYS[request_index])
            print("\n" + "-" * 20)
            print(result)
            print("\n" + "-" * 20)
