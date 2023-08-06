#!./python/bin/python3
# -*- coding: UTF-8 -*-


import os
import datetime
import logging
import logging.handlers
import colour


def get_default_log_file(logger_name, product_name='default'):
    log_dir = os.path.join("/tmp/logs", product_name)
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, '%s.log' % logger_name)


def init_logger(logger_name, log_file, console_level, file_format, max_file_size=1024 * 1024, max_file_num=10):
    if not log_file:
        log_file = get_default_log_file(logger_name)
    # 配置logger整体
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # 配置console 打印INFO级别
    console = logging.StreamHandler()
    console.setLevel(console_level)
    console.setFormatter(colour.ColouredFormatter('%(asctime)s %(levelname)s %(message)s'))
    logger.addHandler(console)

    # 单个文件最大1m 最多10个文件
    fa = logging.handlers.RotatingFileHandler(log_file, 'a', max_file_size, max_file_num)
    fa.setLevel(logging.DEBUG)
    formater = logging.Formatter(file_format)
    fa.setFormatter(formater)
    logger.addHandler(fa)

    return logger


def init_runtime_logger(product, logger_name):
    """
    初始化日志到runtime 目录
    """
    log_dir = os.path.join('/tmp/logs', product, logger_name)
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    file_format = '%(asctime)s %(levelname)s %(lineno)d [%(process)d:%(threadName)s] %(message)s'
    return log_file, init_logger(logger_name, log_file, logging.INFO, file_format)
