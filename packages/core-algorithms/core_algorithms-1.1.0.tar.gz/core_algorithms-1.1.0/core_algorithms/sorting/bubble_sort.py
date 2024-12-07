# -*- coding: utf-8 -*-

from typing import List


def bubble_sort(array: List):
    def swap(x: int, y: int):
        array[x], array[y] = array[y], array[x]

    n = len(array)
    swapped = True
    pos = -1

    while swapped:
        swapped = False
        pos = pos + 1
        for i in range(1, n - pos):
            if array[i - 1] > array[i]:
                swap(i - 1, i)
                swapped = True

    return array
