import time

import fire
from core import LMSDriver


def automation(username, password):
    driver = LMSDriver(username, password)
    driver.check()


if __name__ == '__main__':
    fire.Fire(automation)
