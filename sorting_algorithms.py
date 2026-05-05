import time

def bubble_sort(arr, draw_func, speed, comparisons, swaps, colors):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons[0] += 1
            
            # Highlight comparing elements
            color_array = [colors['bar_default']] * len(arr)
            color_array[j] = colors['bar_comparing']
            color_array[j + 1] = colors['bar_comparing']
            
            if j + i + 1 < n:
                for k in range(j + i + 1, n):
                    color_array[k] = colors['bar_sorted']
            
            draw_func(arr, color_array)
            time.sleep(speed)
            
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps[0] += 1


def selection_sort(arr, draw_func, speed, comparisons, swaps, colors):
    n = len(arr)
    for i in range(n):
        min_idx = i
        
        for j in range(i + 1, n):
            comparisons[0] += 1
            
            # Highlight current minimum and comparing element
            color_array = [colors['bar_default']] * len(arr)
            for k in range(i):
                color_array[k] = colors['bar_sorted']
            color_array[min_idx] = colors['bar_comparing']
            color_array[j] = colors['bar_comparing']
            
            draw_func(arr, color_array)
            time.sleep(speed)
            
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps[0] += 1


def insertion_sort(arr, draw_func, speed, comparisons, swaps, colors):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            comparisons[0] += 1
            
            arr[j + 1] = arr[j]
            swaps[0] += 1
            
            # Highlight
            color_array = [colors['bar_default']] * len(arr)
            for k in range(i + 1):
                color_array[k] = colors['bar_sorted']
            color_array[j] = colors['bar_comparing']
            color_array[j + 1] = colors['bar_comparing']
            
            draw_func(arr, color_array)
            time.sleep(speed)
            
            j -= 1
        
        arr[j + 1] = key


def merge_sort(arr, left, right, draw_func, speed, comparisons, swaps, colors):
    if left < right:
        mid = (left + right) // 2
        
        merge_sort(arr, left, mid, draw_func, speed, comparisons, swaps, colors)
        merge_sort(arr, mid + 1, right, draw_func, speed, comparisons, swaps, colors)
        merge(arr, left, mid, right, draw_func, speed, comparisons, swaps, colors)


def merge(arr, left, mid, right, draw_func, speed, comparisons, swaps, colors):
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    while i < len(left_part) and j < len(right_part):
        comparisons[0] += 1
        
        color_array = [colors['bar_default']] * len(arr)
        color_array[k] = colors['bar_comparing']
        draw_func(arr, color_array)
        time.sleep(speed)
        
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        swaps[0] += 1
        k += 1
    
    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1
        swaps[0] += 1
    
    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1
        swaps[0] += 1


def quick_sort(arr, low, high, draw_func, speed, comparisons, swaps, colors):
    if low < high:
        pi = partition(arr, low, high, draw_func, speed, comparisons, swaps, colors)
        quick_sort(arr, low, pi - 1, draw_func, speed, comparisons, swaps, colors)
        quick_sort(arr, pi + 1, high, draw_func, speed, comparisons, swaps, colors)


def partition(arr, low, high, draw_func, speed, comparisons, swaps, colors):
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        comparisons[0] += 1
        
        color_array = [colors['bar_default']] * len(arr)
        color_array[high] = colors['bar_sorted']  # Pivot
        color_array[j] = colors['bar_comparing']
        if i >= 0:
            color_array[i] = colors['bar_comparing']
        
        draw_func(arr, color_array)
        time.sleep(speed)
        
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            swaps[0] += 1
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    swaps[0] += 1
    return i + 1


def heap_sort(arr, draw_func, speed, comparisons, swaps, colors):
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, draw_func, speed, comparisons, swaps, colors)
    
    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        swaps[0] += 1
        
        color_array = [colors['bar_default']] * len(arr)
        for j in range(i, n):
            color_array[j] = colors['bar_sorted']
        color_array[0] = colors['bar_comparing']
        
        draw_func(arr, color_array)
        time.sleep(speed)
        
        heapify(arr, i, 0, draw_func, speed, comparisons, swaps, colors)


def heapify(arr, n, i, draw_func, speed, comparisons, swaps, colors):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n:
        comparisons[0] += 1
        if arr[left] > arr[largest]:
            largest = left
    
    if right < n:
        comparisons[0] += 1
        if arr[right] > arr[largest]:
            largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        swaps[0] += 1
        
        color_array = [colors['bar_default']] * len(arr)
        color_array[i] = colors['bar_comparing']
        color_array[largest] = colors['bar_comparing']
        
        draw_func(arr, color_array)
        time.sleep(speed)
        
        heapify(arr, n, largest, draw_func, speed, comparisons, swaps, colors)
