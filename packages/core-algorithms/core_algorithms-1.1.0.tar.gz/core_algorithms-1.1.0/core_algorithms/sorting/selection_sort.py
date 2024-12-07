# -*- coding: utf-8 -*-

from typing import List


def selection_sort(array: List):
    for i in range(len(array)):
        minimum = i
        for j in range(i + 1, len(array)):
            # Select the smallest value...
            if array[j] < array[minimum]:
                minimum = j

        # Place it at the front of the sorted end of the array...
        array[minimum], array[i] = array[i], array[minimum]

    return array
