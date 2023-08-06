from .oai import prompt as oai_prompt
from .generate_func import FunctionGenerator
from .generate_pytest import PytestGenerator
from .generate_docstring import DocstringGenerator
from .generate_expansion import SearchExpansionGenerator


def generate_function(*file_names):
    return FunctionGenerator(oai_prompt).generate(*file_names)


def generate_docstring(*file_names):
    return DocstringGenerator(oai_prompt).generate(*file_names)


def generate_pytest(*file_names):
    return PytestGenerator(oai_prompt).generate(*file_names)


def generate_search_expansion(*file_names):
    return SearchExpansionGenerator(oai_prompt).generate(*file_names)


def generate_analysis(file_name):
    print(f"Analyzing {file_name}")
