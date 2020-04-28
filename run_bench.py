import os
from math import nan
from subprocess import run, DEVNULL
import sys
from datetime import datetime
from collections import defaultdict

benchmarks = [x for x in os.listdir() if x.startswith('bench_')]

orig_dir = os.getcwd()

runners = [
    'pytest',
    'nose2',
    'hammett',
]

unsupported = {
    'hammett': set(),
    'pytest': set(),
    'nose2': {'bench_many_folders'},
}

results = defaultdict(lambda: defaultdict(dict))


def run_bench(runner):
    for bench in benchmarks:
        if bench in unsupported[runner]:
            print(runner, 'MISSING FEATURE', bench)
            results[bench][runner] = 0
            continue
        os.chdir(orig_dir)
        runner_specific = f'{bench}__{runner}'

        bench_dir = bench
        if os.path.exists(runner_specific):
            bench_dir = runner_specific

        os.chdir(bench_dir)
        print(runner, bench)
        start = datetime.now()
        run([sys.executable, '-m', runner], stdout=DEVNULL, stderr=DEVNULL)
        results[bench][runner] = int((datetime.now() - start).total_seconds() * 1000)


print('Running...')

for runner in runners:
    run_bench(runner)
    run_bench(runner)


print()

from termgraph.termgraph import chart, print_categories


data = [
    list(x.values())
    for x in results.values()
]
args = {
    'filename': 'data/ex1.dat',
    'title': None,
    'width': 10,
    'format': '{} ms',
    'suffix': '',
    'no_labels': False,
    'color': None,
    'vertical': False,
    'stacked': False,
    'different_scale': False,
    'calendar': False,
    'start_dt': None,
    'custom_tick': '',
    'delim': '',
    'verbose': False,
    'version': False
}
labels = list(results.keys())

colors = [91, 94, 92]
print_categories(runners, colors)
chart(colors, data, args, labels)
