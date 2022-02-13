import os
import random
import time

import fire
import yaml
from crontab import CronTab

from core import LMSDriver

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, 'config.yml'), 'r') as f:
    CFG = yaml.safe_load(f)


def check(course_id=None, username: str = CFG['credentials']['username'],
          password: str = CFG['credentials']['password'],
          tries: int = 1):
    if tries <= 0:
        return
    now = time.time()
    driver = LMSDriver(CFG['paths']['chromedriver'], username, password, CFG['paths']['url'])
    try:
        if course_id:
            driver.go_to_course_last_event(course_id)
        else:
            driver.go_to_last_event()
    except Exception as e:
        print(e)
        if time.time() - now > 60 * 10:
            driver.driver.quit()
            return
        time.sleep(random.random() * 60)
        check(course_id, username, password, tries - 1)


def add(scheduler: bool = False, user=True):
    tab = ''
    for course in CFG['courses']:
        for cron in course['crons']:
            tab += '{} {} {} check {} >{} 2>{} # autolms'.format(
                cron,
                CFG['paths']['python3'],
                CFG['paths']['main'],
                course['id'],
                CFG['paths']['stdout'], CFG['paths']['stderr']
            ) + '\n'
    cron = CronTab(tab=tab)
    if scheduler:
        for _ in cron.run_scheduler():
            print("Doing...")
    else:
        reset(user)
        cron.write(user=user)


def show(user=True):
    cron = CronTab(user=user)
    for job in cron:
        print(job)


def reset(user=True):
    cron = CronTab(user=user)
    cron.remove_all(comment='autolms')
    cron.write()


if __name__ == '__main__':
    fire.Fire({
        'check': check,
        'add': add,
        'show': show,
        'reset': reset
    })
