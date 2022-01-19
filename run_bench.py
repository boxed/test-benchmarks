import os
from io import StringIO
from subprocess import (
    CalledProcessError,
    check_output,
    PIPE,
    run,
    DEVNULL,
)
import sys
from datetime import datetime
from collections import defaultdict

import colorama

benchmarks = [x for x in os.listdir() if x.startswith('bench_') and '__' not in x]

selected_benchmarks = sys.argv[1:]

if sys.argv[1:]:
    for x in selected_benchmarks:
        if x not in benchmarks:
            print(f'{x} not in available benchmarks. Valid values are: {benchmarks}')
            exit(1)

    benchmarks = selected_benchmarks

orig_dir = os.getcwd()

runners = {
    'pytest': colorama.Fore.RED,
    'ward': colorama.Fore.YELLOW,
    'nose2': colorama.Fore.CYAN,
    'hammett': colorama.Fore.GREEN,
}

unsupported = {
    'hammett': set(),
    'pytest': set(),
    'ward': {'bench_parametrize_slow_fixture', 'bench_parametrize_slow_session_fixture'},
    'nose2': {'bench_many_folders'},
}

results = defaultdict(lambda: defaultdict(dict))

# make sure hammett isn't cheating!
for root, dirs, files in os.walk('.'):
    for filename in files:
        if filename == '.hammett-db':
            os.remove(os.path.join(root, filename))


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

        command = [sys.executable, '-m', runner]
        if runner == 'ward':
            command.append('--path')
            command.append('.')

        r = run(command, stdout=PIPE, stderr=PIPE)
        output = r.stderr + b'\n' + r.stdout
        if 'no_tests' not in bench:
            # Wards error for no tests found
            if b'NO_TESTS_FOUND' in output:
                results[bench][runner] = 0
                continue

            # nose2s error for no tests found
            if b'Ran 0 tests' in output:
                results[bench][runner] = 0
                continue

        results[bench][runner] = int((datetime.now() - start).total_seconds() * 1000)


print('Running...')

for runner in runners:
    run_bench(runner)


print()

block = '▇'

for runner, color in runners.items():
    print(f'{color}{block}{colorama.Style.RESET_ALL} {runner}')

print()
print()

terminal_width = os.get_terminal_size()[0]

for bench_name, bench_results in results.items():
    title = bench_name.replace('bench_', '').replace('_', ' ').capitalize()
    print(title)
    print('-' * len(title))
    print()

    max_width = max(bench_results.values())

    for runner, ms in bench_results.items():
        width = int(ms / max_width * (terminal_width - len('123456 ms ') - 1))
        if ms == 0:
            ms = 'N/A'
        print(f'{ms:>6} ms {runners[runner]}{block * width}{colorama.Style.RESET_ALL}')

    print()
    print()
