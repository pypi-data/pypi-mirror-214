from functools import partial
from itertools import product
from mtmtool.log import create_stream_logger
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os

logger = create_stream_logger("Pool")

CPUNUM = os.cpu_count()


def parfunc(func, *args, **kargs):
    return partial(func, *args, **kargs)


""" 
map 与 starmap 函数的区别:
    map只展开一次, 只能向函数掺入一个参数
    starmap可展开两次, 可以向函数传入多个参数
product 函数:
    输入多个可迭代参数, 返回所有笛卡尔积元组
"""


def pool_process(par_func, iterables, worker_num=CPUNUM):
    with Pool(worker_num) as p:
        res_list = p.map(par_func, iterables)
    return res_list


def pool_thread(par_func, iterables, worker_num=CPUNUM):
    with ThreadPool(worker_num) as p:
        res_list = p.map(par_func, iterables)
    return res_list


def starmap(func, *args, is_test=False, worker_num=None, ptype="Process"):
    """输入args必须可迭代
    usage:
        >>> result = starmap(pow, [10,15], [3,5], worker_num=4, ptype="Thread")
        >>> result
        [1000, 100000, 3375, 759375]
    """
    iters = product(*args)
    pool = Pool if ptype == "Process" else ThreadPool
    worker_num = CPUNUM if worker_num is None else worker_num
    if is_test:
        res = []
        for args_t in iters:
            res.append(func(*args_t))
    else:
        with pool(worker_num) as p:
            res = p.starmap(func, iters)
    return res


class MapPool:
    def __init__(self, function=None, max_workers=None, ptype="Thread") -> None:
        self.max_workers = max_workers
        self.buffer = []
        self.set_function(function)
        self.pool = ProcessPoolExecutor if ptype == "Process" else ThreadPoolExecutor

    def __call__(self, *args, **kwargs):
        self.buffer.append((args, kwargs))
        pass

    def set_function(self, func):
        self.function = func

    def worker_wrapper(self, arg):
        args, kwargs = arg
        return self.function(*args, **kwargs)

    def result(self):
        logger.info("Start running with {} workers, {} tasks".format(self.max_workers, len(self.buffer)))
        with self.pool(max_workers=self.max_workers) as executor:
            res = executor.map(self.worker_wrapper, self.buffer)
        self.buffer = []
        return res