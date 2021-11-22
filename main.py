import fire
import yaml
from core import LMSDriver
from crontab import CronTab
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + '/config.yml', 'r') as f:
    CFG = yaml.safe_load(f)


def check(username: str = CFG['credentials']['username'], password: str = CFG['credentials']['password']):
    driver = LMSDriver(CFG['paths']['chromedriver'], username, password)
    driver.go_to_last_event()


def schedule():
    tab = ''
    for cron in CFG['schedule']:
        tab += '{} {} {} check >{} 2>{} # autolms\n'.format(cron, CFG['paths']['python3'], __file__,
                                                            CFG['paths']['stdout'], CFG['paths']['stderr'])
    reset()
    cron = CronTab(tab=tab)
    cron.write(user=True)


def show():
    cron = CronTab(user=True)
    for job in cron:
        print(job)


def reset():
    cron = CronTab(user=True)
    cron.remove_all()
    cron.write()


if __name__ == '__main__':
    fire.Fire({
        'check': check,
        'schedule': schedule,
        'show': show,
        'reset': reset
    })
