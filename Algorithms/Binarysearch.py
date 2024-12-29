def binarysearch(array, key):

    left = 0
    right = len(array) - 1
    count = 0

    while left <= right:
        count = count + 1
        middle = (left + right) // 2
        if key == array[middle]:
            return middle, count
        elif key < array[middle]:
            right = middle - 1
        else:
            left = middle + 1
    return - 1, count


class Test:

    unsorted_max_left = [5, 9, 1, 0, 11, 487, 56, 6, 12, 71, 15, 85, 47, 2, 51, 68, 16]
    unsorted_max_right = [18, 28, 57, 14, 15, 7, 8, 5, 3, 4, 1, 45, 78, 0, 56, 2, 1456]

    sorted_max_left = sorted(unsorted_max_left)
    sorted_max_right = sorted(unsorted_max_right)

    sort = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    duplicate = [0, 1, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 9]

    nokey = [3, 14, 27, 31, 39, 42, 55, 70, 74, 81, 85, 93, 98]

    long = list(range(0, 1001))
    short = [0, 1, 2, 3]

    sorted_max_leftIndex = binarysearch(sorted_max_left, max(sorted_max_left))
    sorted_max_rightIndex = binarysearch(sorted_max_right, max(sorted_max_right))

    sorted_min_leftIndex = binarysearch(sorted_max_left, min(sorted_max_left))
    sorted_min_rightIndex = binarysearch(sorted_max_right, min(sorted_max_right))

    sortedIndex = binarysearch(sort, 3)

    duplicateIndex = binarysearch(duplicate, 9)

    long_leftIndex = binarysearch(long, 0)
    long_rightIndex = binarysearch(long, 1000)
    long_midIndex = binarysearch(long, 500)

    shortIndex = binarysearch(short, 0)

    no_keyIndex = binarysearch(nokey, 100)
    middleIndex = binarysearch(sort, 5)

    # Sorted Arrays Max Element (487 for first array, 1456 for second array)

    if sorted_max_leftIndex[0] != -1:
        print('\n',sorted_max_left)
        print("The index of sorted array max element",
              sorted_max_left[sorted_max_leftIndex[0]], "is:", sorted_max_leftIndex[0],
              'iterated:', sorted_max_leftIndex[1], 'times', '\n')
    else:
        print('\n', sorted_max_left)
        print("Index not found for sorted array max element:", sorted_max_leftIndex[0],
              'iterated:', sorted_max_leftIndex[1], 'times', '\n')

    if sorted_max_rightIndex[0] != -1:
        print(sorted_max_right)
        print("The index of sorted array with element",
              sorted_max_right[sorted_max_rightIndex[0]], "is:", sorted_max_rightIndex[0],
              'iterated:', sorted_max_rightIndex[1], 'times', '\n')
    else:
        print(sorted_max_right)
        print("Index not found for sorted array max element:", sorted_max_rightIndex[0],
              'iterated:', sorted_max_rightIndex[1], 'times', '\n')

    # Sorted Arrays Min Element (0 for both arrays)

    if sorted_min_leftIndex[0] != -1:
        print(sorted_max_left)
        print("The index of sorted array min element",
              sorted_max_left[sorted_min_leftIndex[0]], "is:", sorted_min_leftIndex[0],
              'iterated:', sorted_min_leftIndex[1], 'times', '\n')
    else:
        print(sorted_max_left)
        print("Index not found for sorted array min element:", sorted_min_leftIndex[0],
              'iterated:', sorted_min_leftIndex[1], 'times', '\n')

    if sorted_min_rightIndex[0] != -1:
        print(sorted_max_right)
        print("The index of sorted array min element",
              sorted_max_right[sorted_min_rightIndex[0]], "is:", sorted_min_rightIndex[0],
              'iterated:', sorted_min_rightIndex[1], 'times', '\n')
    else:
        print(sorted_max_right)
        print("Index not found for sorted array min element:", sorted_min_rightIndex[0],
              'iterated:', sorted_min_leftIndex[1], 'times', '\n')

    # Sorted array (key is 3)

    if sortedIndex[0] != -1:
        print(sort)
        print("The index of sorted array element",
              sort[sortedIndex[0]], "is:", sortedIndex[0],
              'iterated:', sortedIndex[1], 'times', '\n')
    else:
        print(sort)
        print("Index not found for sorted array:", sortedIndex[0],
              'iterated:', sortedIndex[1], 'times', '\n')

    # Duplicate array (key is 9)

    if duplicateIndex[0] != -1:
        print(duplicate)
        print("The index of duplicate array element",
              duplicate[duplicateIndex[0]], "is:", duplicateIndex[0],
              'iterated:', duplicateIndex[1], 'times', '\n')
    else:
        print(duplicate)
        print("Index not found for duplicate array:", duplicateIndex[0],
              'iterated:', duplicateIndex[1], 'times', '\n')

    # Key Not in Element (Worst Case)

    if no_keyIndex[0] != -1:
        print(nokey)
        print("The index of no key in array element",
              sort[no_keyIndex[0]], "is:", no_keyIndex[0],
              'iterated:', no_keyIndex[1], 'times', '\n')
    else:
        print(nokey)
        print("Index not found for no key array:", no_keyIndex[0],
              'iterated:', no_keyIndex[1], 'times', '\n')

    # Middle Element key (Best Case)

    if middleIndex[0] != -1:
        print(sort)
        print("The index of the middle element in array",
              sort[middleIndex[0]], "is:", middleIndex[0],
              'iterated:', middleIndex[1], 'times', '\n')
    else:
        print(sort)
        print("Index not found for middle element in array:", middleIndex[0],
              'iterated:', middleIndex[1], 'times', '\n')

    # Short array (Element 0)

    if shortIndex[0] != -1:
        print(short)
        print("The index of short array element",
              short[shortIndex[0]], "is:", shortIndex[0],
              'iterated:', shortIndex[1], 'times', '\n')
    else:
        print(short)
        print("Index not found for short array:", shortIndex[0],
              'iterated:', shortIndex[1], 'times', '\n')

    # Long Array Left Side, Middle, Right Side (0, 500, 1000)

    if long_leftIndex[0] != -1:
        print("The index of left side long array element",
              long[long_leftIndex[0]], "is:", long_leftIndex[0],
              'iterated:', long_leftIndex[1], 'times',)
    else:
        print("Index not found for left side long array:", long_leftIndex[0],
              'iterated:', long_leftIndex[1], 'times',)

    if long_midIndex[0] != -1:
        print("The index of middle long array element",
              long[long_midIndex[0]], "is:", long_midIndex[0],
              'iterated:', long_midIndex[1], 'times',)
    else:
        print("Index not found for middle long array:", long_midIndex[0],
              'iterated:', long_midIndex[1], 'times',)

    if long_rightIndex[0] != -1:
        print("The index of right side long array element",
              long[long_rightIndex[0]], "is:", long_rightIndex[0],
              'iterated:', long_rightIndex[1], 'times', '\n')
    else:
        print("Index not found for right side long array:", long_rightIndex[0],
              'iterated:', long_rightIndex[1], 'times', '\n')
        
    print(long)
