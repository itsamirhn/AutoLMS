import datetime
import time

import fire
import schedule

import config
from core import LMSDriver


def check(chromedriver, username, password, url, course_id=None):
    driver = LMSDriver(chromedriver, username, password, url)
    if course_id:
        driver.go_to_course_last_event(course_id)
    else:
        driver.go_to_last_event()


def go(course_id=None):
    cfg = config.get_config()
    if not cfg:
        print("Run `setup` command for config first.")
        return
    chromedriver = cfg["paths"]["chromedriver"]
    username = cfg["credentials"]["username"]
    password = cfg["credentials"]["password"]
    url = cfg["credentials"]["url"]
    try:
        print("Checking...")
        check(chromedriver, username, password, url, course_id)
    except Exception as e:
        print(e)
        print("End")


def setup():
    config.setup()
    print("You can use `run` command now.")


def edit():
    config.edit()
    print("You can use `run` command now.")


def run():
    cfg = config.get_config()
    if not cfg:
        print("Run `setup` command for config first.")
        return
    for course in cfg["courses"]:
        for session in course["sessions"]:
            session_time = datetime.datetime.strptime(session["time"], "%H:%M") \
                           - datetime.timedelta(seconds=int(cfg["options"]["rush"]))
            rushed_time = session_time.strftime("%H:%M:%S")
            getattr(schedule.every(), session["day"]).at(rushed_time).do(go, course_id=course["id"])
            print("Add job for %s on %s at %s" % (course["name"], session["day"], rushed_time))
    print("Running schedule...")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    fire.Fire({
        "go": go,
        "run": run,
        "setup": setup,
        "edit": edit,
    })
