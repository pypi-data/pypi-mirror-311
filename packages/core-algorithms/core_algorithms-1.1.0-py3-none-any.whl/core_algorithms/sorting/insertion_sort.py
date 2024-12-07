# -*- coding: utf-8 -*-

from typing import List


def insertion_sort(array: List):
    for i in range(len(array)):
        cursor, pos = array[i], i
        while pos > 0 and array[pos - 1] > cursor:
            array[pos] = array[pos - 1]
            pos = pos - 1

        array[pos] = cursor

    return array
