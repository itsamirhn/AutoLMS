import re
import time
from pathlib import Path

import yaml
from InquirerPy import inquirer, prompt
from InquirerPy.base import Choice
from InquirerPy.validator import PathValidator, NumberValidator

yml_path = Path('config.yml')

credentials_questions = [
    {
        "type": "list",
        "name": "url",
        "message": "Select your university:",
        "choices": [
            Choice("https://lms.khu.ac.ir", name="Kharazmi"),
        ],
    },
    {
        "type": "input",
        "name": "username",
        "message": "Enter your LMS Username:",
        "validate": lambda x: len(x) > 0,
    },
    {
        "type": "password",
        "name": "password",
        "message": "Enter your LMS Password:",
        "validate": lambda x: len(x) > 0,
    }
]

options_questions = [
    {
        "type": "number",
        "name": "rush",
        "message": "How many seconds earlier you want to get into the class:",
        "min_allowed": 0,
        "default": 30,
    },
]

course_questions = [
    {
        "type": "input",
        "name": "name",
        "message": "Enter new Course Name:",
        "validate": lambda x: len(x) > 0,
        "long_instruction": "Your custom a name for calling this course (e.g. Advanced Programming)",
    },
    {
        "type": "input",
        "name": "id",
        "message": "Enter Course ID in LMS:",
        "validate": NumberValidator(),
        "long_instruction": "For example for a course like `http://lms.com/course/view.php?id=1194`, id is `1194`",
    },
    {
        "type": "list",
        "name": "day",
        "message": "Select a new Session Day:",
        "choices": [
            Choice("saturday", name="Saturday"),
            Choice("sunday", name="Sunday"),
            Choice("monday", name="Monday"),
            Choice("tuesday", name="Tuesday"),
            Choice("wednesday", name="Wednesday"),
            Choice("thursday", name="Thursday"),
            Choice("friday", name="Friday"),
        ],
    },
    {
        "type": "input",
        "name": "time",
        "message": "Enter the Session Time:",
        "instruction": "(HH:MM Format)",
        "validate": lambda x: re.match(r"^([0-2]\d:)?[0-5]\d:[0-5]\d$", x)
    },
]

paths_questions = [
    {
        "type": "filepath",
        "message": "Enter chromedriver path:",
        "name": "chromedriver",
        "validate": PathValidator(is_file=True, message="Input is not a file"),
        "only_files": True,
        "filter": lambda file: str(Path(file).absolute()),
    },
]


def validate_time(text):
    try:
        time.strptime(text, "%H:%M")
        return True
    except:
        return False


def prompt_course():
    course = prompt(course_questions[:2])
    course["sessions"] = []
    finished = False
    while not finished:
        course["sessions"].append(prompt(course_questions[2:]))
        finished = inquirer.confirm("Are you finished adding Sessions for %s course ?" % course["name"],
                                    default=True).execute()
    return course


def prompt_config():
    if Path(yml_path).exists():
        if not inquirer.confirm("A Config already exists, Do you want to reset it?").execute():
            return None
    config = {
        "credentials": prompt(credentials_questions),
        "paths": prompt(paths_questions),
        "options": prompt(options_questions),
        "courses": []
    }
    finished = False
    while not finished:
        config["courses"].append(prompt_course())
        finished = inquirer.confirm("Are you finished?", default=True).execute()
    return config


def setup():
    config = prompt_config()
    if not config:
        return
    with open(yml_path, 'w+') as f:
        yaml.safe_dump(config, f)
    return config


def get_config():
    if Path(yml_path).exists():
        with open(yml_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    else:
        return None
