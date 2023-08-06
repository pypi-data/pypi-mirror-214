import logging
from datetime import datetime, date
import os
import wandb

def init_wandb(offline=False, config=None, params=None):
    if offline:
        os.environ['WANDB_MODE'] = 'offline'

    wandb.login(relogin=True)
    if "few-shot-size" in params:
        wandb.init(project=f"few-shot-stance-cls-{config['few-shot-size']}", config=params, name=f"{config['model-name']}-batch-size-{params['batch-size']}-learning-rate-{params['learning-rate']}")
    else:
        wandb.init(project=f"few-shot-stance-cls", config=params, name=f"{config['model-name']}-batch-size-{params['batch-size']}-learning-rate-{params['learning-rate']}")


def setup_logging(logger_name, path, level):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    print(f"current working directory is {os.getcwd()}")
    print(f"path of log file {path}")
    fh = logging.FileHandler(path)
    fh.setLevel(level)
    formatter = logging.Formatter('%(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    now=datetime.now()
    logger.info(now.strftime("%Y-%m-%d %H:%M")+"\n")

def log_message(logger_name, message, level=logging.WARNING):
    logger = logging.getLogger(logger_name)
    now=datetime.now()
    if level == logging.INFO:
        logger.info(now.strftime("%H:%M")+"\t" + message)
    else:
        logger.warning(now.strftime("%H:%M")+"\t" + message)