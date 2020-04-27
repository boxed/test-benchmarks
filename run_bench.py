import os
from subprocess import run, DEVNULL
import sys
from datetime import datetime
from collections import defaultdict

benchmarks = [x for x in os.listdir() if x.startswith('bench_')]

orig_dir = os.getcwd()

runners = [
    'hammett',
    'pytest',
]

results = defaultdict(lambda: defaultdict(dict))


def run_bench(runner):
    for bench in benchmarks:
        os.chdir(orig_dir)
        os.chdir(bench)
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
    'width': 50,
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

colors = [94, 91, 0]
print_categories(runners, colors)
chart(colors, data, args, labels)
