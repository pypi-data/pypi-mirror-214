import logging, json
from .util import read_source_files, get_code

USER_REQUEST = (
    "Generate high quality unit tests using the pytest unit testing framework "
    "for all the functions and class methods."
)


class PytestGenerator:
    def __init__(self, prompt):
        self._prompt = prompt

    def generate(self, *file_names):
        source_code = read_source_files(*file_names)
        logging.debug(f"Generating unit tests...")
        result = self._prompt(source_code, USER_REQUEST)
        return get_code(result, "code")
