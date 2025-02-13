def quick_sort(arr):
    """
    QuickSort Algorithm: Sorts an array using the divide-and-conquer strategy.
    
    Parameters:
    - arr: List of integers or floats to be sorted.
    
    Returns:
    - A new sorted list.
    """
    # Base case: Arrays with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr
    
    # Step 1: Select a pivot element
    # Here, we choose the middle element as the pivot for simplicity.
    pivot = arr[len(arr) // 2]
    
    # Step 2: Partition the array into three parts:
    # - Left: Elements less than the pivot
    # - Middle: Elements equal to the pivot
    # - Right: Elements greater than the pivot
    left = [x for x in arr if x < pivot]    # Elements smaller than pivot
    middle = [x for x in arr if x == pivot] # Elements equal to pivot
    right = [x for x in arr if x > pivot]   # Elements larger than pivot
    
    # Step 3: Recursively apply QuickSort to the left and right partitions
    # Concatenate the results to form the sorted array
    return quick_sort(left) + middle + quick_sort(right)


# Example usage
if __name__ == "__main__":
    # Input array
    array = [10, 7, 8, 9, 1, 5, 7, 3]
    
    # Output the sorted array
    print("Original array:", array)
    print("Sorted array:", quick_sort(array))
