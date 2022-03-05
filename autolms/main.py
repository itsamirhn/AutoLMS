import datetime
import time

import fire
import schedule

import autolms.config as config
from autolms.core import LMSDriver

events = []


def check(chromedriver, username, password, url, course_id=None):
    driver = LMSDriver(chromedriver, username, password, url)
    if course_id:
        driver.go_to_course_last_event(course_id)
    else:
        driver.go_to_last_event()


def go(course_id=None, course_name=None):
    cfg = config.get_config()
    if not cfg:
        print("Run `setup` command for config first.")
        return
    if not course_name:
        course_name = course_id
    chromedriver = cfg["paths"]["chromedriver"]
    username = cfg["credentials"]["username"]
    password = cfg["credentials"]["password"]
    url = cfg["credentials"]["url"]
    try:
        print(f"Starting {course_name}...")
        check(chromedriver, username, password, url, course_id)
    except Exception as e:
        print(e)
    finally:
        events.append({"status": "finish", "name": course_name, "id": course_id})
        print("Finish")


def setup():
    if config.setup():
        print("You can use `run` command now.")


def edit():
    if config.edit():
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
            getattr(schedule.every(), session["day"]).at(rushed_time).do(go, course_id=course["id"],
                                                                         course_name=course["name"])
            print("Add job for %s on %s at %s" % (course["name"], session["day"], rushed_time))
    print("Running schedule...")
    while True:
        schedule.run_pending()
        while len(events) > 0:
            yield events.pop(0)
        time.sleep(1)


def main():
    fire.Fire({
        "go": go,
        "run": run,
        "setup": setup,
        "edit": edit,
    })


if __name__ == "__main__":
    main()
