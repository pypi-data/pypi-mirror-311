import os
import threading

from aliyun_log_py_bindings import log_parser

workdir = os.getenv("BENCHMARK_TEST_WORKDIR")

with open(os.path.join(workdir, 'compressed.data'), 'rb') as f:
    compressed = f.read()

with open(os.path.join(workdir, 'rawdata.data'), 'rb') as f:
    rawdata = f.read()

raw_size = len(rawdata)
with open(os.path.join(workdir, 'flat.json'), 'r') as f:
    json_str = f.read()


def lz4_logs_to_flat_json():
    log_parser.lz4_logs_to_flat_json(compressed, raw_size, False, True)


def test_lz4_logs_to_flat_json(benchmark):
    result = benchmark(lz4_logs_to_flat_json)


def logs_to_flat_json_str():
    log_parser.logs_to_flat_json_str(rawdata)


def test_logs_to_flat_json_str(benchmark):
    result = benchmark(logs_to_flat_json_str)


def lz4_logs_to_flat_json_str():
    log_parser.lz4_logs_to_flat_json_str(compressed, raw_size)


def test_lz4_logs_to_flat_json_str(benchmark):
    result = benchmark(lz4_logs_to_flat_json_str)


def multi_threaded_task(num_threads, func):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def test_lz4_logs_to_flat_json_n_threads():
    multi_threaded_task(4, lz4_logs_to_flat_json)
