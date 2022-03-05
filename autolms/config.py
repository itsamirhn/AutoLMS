import os
import re
import time
from pathlib import Path

import yaml
from InquirerPy import inquirer, prompt
from InquirerPy.base import Choice
from InquirerPy.separator import Separator
from InquirerPy.utils import color_print
from InquirerPy.validator import PathValidator

yml_path = Path('config.yml')


def find(name, path, tl=None):
    path = str(Path(path).absolute())
    start = time.time()
    for root, dirs, files in os.walk(path):
        if tl and time.time() >= start + tl:
            return False
        if name in files:
            return os.path.join(root, name)
    return None


def find_chromedriver(tl):
    chromedriver = "chromedriver"
    if os.name == 'nt':
        chromedriver = "chromedriver.exe"
    paths = [Path.home() / "Downloads", Path.home() / "Desktop", Path("/")]
    start = time.time()
    for path in paths:
        color_print([("#DCE775", f"Searching for {chromedriver} in {path}")])
        f = find(chromedriver, path, tl - (time.time() - start))
        if f:
            color_print([("#00E676", "Found!")])
            return f
    color_print([("#B00020", "Not Found!")])
    return ''


def find_id(url_or_id):
    match = re.search(r"(id=)?(\d+)", url_or_id)
    if match:
        return int(match.group(2))
    return None


credentials_questions = [
    {
        "type": "list",
        "name": "url",
        "message": "Select your university:",
        "choices": [
            Choice("https://elearn5.ut.ac.ir", name="University of Tehran"),
            Choice("https://lms.khu.ac.ir", name="Kharazmi University"),
            Choice("https://lms3.sbu.ac.ir/", name="Shahid Beheshti University"),
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
        "message": "Enter Course ID or just Course URL in LMS:",
        "validate": lambda x: find_id(x) is not None,
        "filter": lambda x: find_id(x),
        "transformer": lambda x: find_id(x),
        "long_instruction": "URL Something like `lms.com/course/view.php?id=1194` or just ID like `1194`",
    }
]

session_questions = [
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
        "long_instruction": "If you don't know what is this, checkout:\n"
                            "https://github.com/itsamirhn/AutoLMS#how-to-download-chromedriver",
        "filter": lambda file: str(Path(file).absolute()),
        "default": lambda _: find_chromedriver(10)
    },
]


def prompt_session():
    session = prompt(session_questions)
    return session


def prompt_course():
    course = prompt(course_questions)
    course["sessions"] = []
    finished = False
    while not finished:
        course["sessions"].append(prompt_session())
        finished = inquirer.confirm("Are you finished adding Sessions for %s course ?" % course["name"],
                                    default=True).execute()
    return course


def prompt_config():
    config = {
        "credentials": prompt(credentials_questions),
        "paths": prompt(paths_questions),
        "options": prompt(options_questions),
        "courses": []
    }
    finished = False
    while not finished:
        config["courses"].append(prompt_course())
        finished = inquirer.confirm("Are you finished adding Courses?", default=True).execute()
    return config


def save_config(config):
    if not config:
        return
    color_print([("#00E676", "New Config saved successfully!")])
    with open(yml_path, 'w+') as f:
        yaml.safe_dump(config, f)


def setup():
    if Path(yml_path).exists():
        if not inquirer.confirm("A Config already exists, Do you want to reset it?").execute():
            return None
    config = prompt_config()
    save_config(config)
    return config


def get_config():
    if Path(yml_path).exists():
        with open(yml_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    else:
        return None


def edit_session(session):
    action = inquirer.select(message="What to you want to do with the Session:",
                             instruction="%s on %s" % (session["time"], session["day"].title()),
                             choices=[
                                 Choice("edit", "Edit this Session"),
                                 Choice("delete", "Delete this Session"),
                             ]).execute()
    if action == "delete":
        return None
    if action == "edit":
        return prompt_session()


def edit_course(course):
    sessions_choices = []
    for index, session in enumerate(course["sessions"]):
        sessions_choices.append(Choice(index, name="%s on %s" % (session["time"], session["day"].title())))
    sessions_choices.append(Separator())
    sessions_choices.append(Choice("add", name="Add new Session"))
    sessions_choices.append(Separator())
    sessions_choices.append(Choice("delete", name="Delete this Course"))
    session_index = inquirer.select(message="Select Session you want to edit:", choices=sessions_choices).execute()
    if session_index == "delete":
        return None
    elif session_index == "add":
        course["sessions"].append(prompt_session())
        return course
    else:
        session = course["sessions"][session_index]
        new_session = edit_session(session)
        if new_session:
            course["sessions"][session_index] = new_session
        else:
            course["sessions"].pop(session_index)
        return course


def edit_config(config):
    sections = inquirer.select(message="Which section do you want to change:", choices=[
        Choice("credentials", name="Credentials"),
        Choice("options", name="Options"),
        Choice("courses", name="Courses"),
    ]).execute()
    if sections == "credentials":
        config["credentials"] = prompt(credentials_questions)
    if sections == "options":
        config["options"] = prompt(options_questions)
    if sections == "courses":
        courses_choices = []
        for index, course in enumerate(config["courses"]):
            courses_choices.append(Choice(index, name=course["name"]))
        courses_choices.append(Separator())
        courses_choices.append(Choice("add", name="Add new Course"))
        course_index = inquirer.select(message="Select Course you want to edit:", choices=courses_choices).execute()
        if course_index == "add":
            config["courses"].append(prompt_course())
        else:
            course = config["courses"][course_index]
            new_course = edit_course(course)
            if new_course:
                config["courses"][course_index] = new_course
            else:
                config["courses"].pop(course_index)
    return config


def edit():
    if not Path(yml_path).exists():
        if inquirer.confirm("No Config already exists, Do you want to create one?", default=True).execute():
            return setup()
        else:
            return None
    config = get_config()
    config = edit_config(config)
    save_config(config)
    return config
