"""
This module is responsible for the handling of 'event_ready' event.
"""

import os

from random import randint


def _cache_and_get(index: int, index_file: str) -> str:
    with open(index_file, 'w') as f:
        f.write(str(index))

    return index


def _get_random_index(bops: list[str]) -> int:
    def random_bop():
        return randint(0, len(bops) - 1)

    chosen_index = random_bop()
    index_file   = os.path.join('greeting', 'index.txt')

    if not os.path.isfile(index_file):
        print('Couldn\'t find the index file. Creating...')
        return _cache_and_get(chosen_index, index_file)

    with open(index_file, 'r') as f:
        previous_index = f.read()

        while chosen_index == previous_index:
            chosen_index = random_bop()
            print(f'Previous bop: {bops[previous_index]}')
            print(f'Current bop: {bops[chosen_index]}')

        return _cache_and_get(chosen_index, index_file)


_bops = (
    'beep bop',
    'bip blip boo bop',
    'boo boo bip bop',
    'whirr bip bip',
    'brrrr brrr',
    'kek kek KEKW',
    'BWAAHH STUTUTUTU',
)


def get_a_bop() -> str:
    global _bops
    return _bops[_get_random_index(_bops)]
