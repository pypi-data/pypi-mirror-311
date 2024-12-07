# -*- coding: utf-8 -*-

from typing import List


def partition(array: List, begin: int, end: int):
    pivot_idx = begin
    for i in range(begin + 1, end + 1):
        if array[i] <= array[begin]:
            pivot_idx += 1
            array[i], array[pivot_idx] = array[pivot_idx], array[i]

    array[pivot_idx], array[begin] = array[begin], array[pivot_idx]
    return pivot_idx


def quick_sort_recursion(array: List, begin: int, end: int):
    if begin >= end:
        return

    pivot_idx = partition(array, begin, end)
    quick_sort_recursion(array, begin, pivot_idx - 1)
    quick_sort_recursion(array, pivot_idx + 1, end)


def quick_sort(array: List, begin=0, end=None):
    if not end:
        end = len(array) - 1

    return quick_sort_recursion(array, begin, end)
