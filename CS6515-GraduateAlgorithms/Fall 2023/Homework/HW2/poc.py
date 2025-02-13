def find_repeated_element(arr, low, high):
    mid = (low + high) // 2

    mid_num = arr[mid]
    left_num = arr[mid - 1]

    if (mid_num == left_num): # repeat number
        return mid
    if (mid_num == mid + 1): # right subarray
        return find_repeated_element(arr, mid + 1, high)
    else: # left subarray
        return find_repeated_element(arr, low, mid - 1)

# Example usage:
A = [1, 2, 3, 4, 4]
result = find_repeated_element(A, 1, len(A) - 1)
print("The repeated element is:", result)


# if high == 0:
    #     return None
    
    # mid = (low + high) // 2

    # left_subarray = [num for num in arr if num <= mid]
    # right_subarray = [num for num in arr if num > mid]

    # count_left = len(left_subarray)
    # count_right = len(right_subarray)
    
    # if count_left > mid:
    #     # The repeated element is in the left subarray
    #     return find_repeated_element(left_subarray, low, mid)
    # elif count_right > high - mid:
    #     # The repeated element is in the right subarray
    #     return find_repeated_element(right_subarray, mid + 1, high)
    # else:
    #     # The repeated element is mid itself
    #     return mid