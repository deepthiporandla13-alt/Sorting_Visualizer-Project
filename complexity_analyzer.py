import matplotlib.pyplot as plt
import numpy as np
import time
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Toplevel, Frame
import tkinter as tk

class ComplexityAnalyzer:
    def __init__(self):
        self.algorithms = {
            'Bubble Sort': self.bubble_sort_time,
            'Selection Sort': self.selection_sort_time,
            'Insertion Sort': self.insertion_sort_time,
            'Merge Sort': self.merge_sort_time,
            'Quick Sort': self.quick_sort_time,
            'Heap Sort': self.heap_sort_time
        }
    
    def bubble_sort_time(self, arr):
        start = time.time()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return time.time() - start
    
    def selection_sort_time(self, arr):
        start = time.time()
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return time.time() - start
    
    def insertion_sort_time(self, arr):
        start = time.time()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return time.time() - start
    
    def merge_sort_time(self, arr):
        start = time.time()
        self._merge_sort(arr, 0, len(arr) - 1)
        return time.time() - start
    
    def _merge_sort(self, arr, left, right):
        if left < right:
            mid = (left + right) // 2
            self._merge_sort(arr, left, mid)
            self._merge_sort(arr, mid + 1, right)
            self._merge(arr, left, mid, right)
    
    def _merge(self, arr, left, mid, right):
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            k += 1
        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1
        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1
    
    def quick_sort_time(self, arr):
        start = time.time()
        self._quick_sort(arr, 0, len(arr) - 1)
        return time.time() - start
    
    def _quick_sort(self, arr, low, high):
        if low < high:
            pi = self._partition(arr, low, high)
            self._quick_sort(arr, low, pi - 1)
            self._quick_sort(arr, pi + 1, high)
    
    def _partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def heap_sort_time(self, arr):
        start = time.time()
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            self._heapify(arr, i, 0)
        return time.time() - start
    
    def _heapify(self, arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self._heapify(arr, n, largest)
    
    def analyze_and_plot(self, algorithm):
        # Create new window
        window = Toplevel()
        window.title(f"Time Complexity Analysis - {algorithm}")
        window.geometry("1000x700")
        window.config(bg='#1e1e2e')
        
        # Title
        title_label = tk.Label(
            window,
            text=f"📊 Time Complexity Analysis: {algorithm}",
            font=('Helvetica', 16, 'bold'),
            bg='#1e1e2e',
            fg='#89b4fa'
        )
        title_label.pack(pady=15)
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.patch.set_facecolor('#1e1e2e')
        
        # Test different array sizes
        sizes = [10, 25, 50, 100, 200, 500]
        times_best = []
        times_avg = []
        times_worst = []
        
        status_label = tk.Label(
            window,
            text="Analyzing... Please wait",
            font=('Helvetica', 11),
            bg='#1e1e2e',
            fg='#f9e2af'
        )
        status_label.pack()
        
        window.update()
        
        for size in sizes:
            # Best case: sorted array
            best_arr = list(range(size))
            times_best.append(self.algorithms[algorithm](best_arr.copy()))
            
            # Average case: random array
            avg_times = []
            for _ in range(3):
                avg_arr = [random.randint(1, 100) for _ in range(size)]
                avg_times.append(self.algorithms[algorithm](avg_arr.copy()))
            times_avg.append(np.mean(avg_times))
            
            # Worst case: reverse sorted array
            worst_arr = list(range(size, 0, -1))
            times_worst.append(self.algorithms[algorithm](worst_arr.copy()))
        
        status_label.config(text="✓ Analysis Complete!")
        
        # Plot 1: Time vs Array Size
        ax1.plot(sizes, times_best, 'go-', label='Best Case', linewidth=2, markersize=8)
        ax1.plot(sizes, times_avg, 'yo-', label='Average Case', linewidth=2, markersize=8)
        ax1.plot(sizes, times_worst, 'ro-', label='Worst Case', linewidth=2, markersize=8)
        ax1.set_xlabel('Array Size', fontsize=12, color='white')
        ax1.set_ylabel('Time (seconds)', fontsize=12, color='white')
        ax1.set_title('Time Complexity Analysis', fontsize=14, color='white', fontweight='bold')
        ax1.legend(facecolor='#2d2d44', edgecolor='white', labelcolor='white')
        ax1.grid(True, alpha=0.3, color='white')
        ax1.set_facecolor('#2d2d44')
        ax1.tick_params(colors='white')
        
        # Plot 2: Bar chart comparison
        x_pos = np.arange(len(sizes))
        width = 0.25
        
        ax2.bar(x_pos - width, times_best, width, label='Best', color='#a6e3a1')
        ax2.bar(x_pos, times_avg, width, label='Average', color='#f9e2af')
        ax2.bar(x_pos + width, times_worst, width, label='Worst', color='#f38ba8')
        
        ax2.set_xlabel('Array Size', fontsize=12, color='white')
        ax2.set_ylabel('Time (seconds)', fontsize=12, color='white')
        ax2.set_title('Comparative Analysis', fontsize=14, color='white', fontweight='bold')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(sizes)
        ax2.legend(facecolor='#2d2d44', edgecolor='white', labelcolor='white')
        ax2.grid(True, alpha=0.3, axis='y', color='white')
        ax2.set_facecolor('#2d2d44')
        ax2.tick_params(colors='white')
        
        plt.tight_layout()
        
        # Embed plot
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Info frame
        info_frame = Frame(window, bg='#2d2d44', relief=tk.RIDGE, bd=2)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        info_text = tk.Label(
            info_frame,
            text=f"📈 Analysis completed for array sizes: {sizes}\n"
                 f"Best case time: {times_best[-1]:.4f}s | "
                 f"Average case time: {times_avg[-1]:.4f}s | "
                 f"Worst case time: {times_worst[-1]:.4f}s",
            font=('Helvetica', 10),
            bg='#2d2d44',
            fg='#cdd6f4',
            justify=tk.LEFT,
            padx=15,
            pady=10
        )
        info_text.pack()
        
        # Close button
        close_btn = tk.Button(
            window,
            text="Close",
            command=window.destroy,
            font=('Helvetica', 11, 'bold'),
            bg='#f38ba8',
            fg='white',
            padx=30,
            pady=10,
            cursor='hand2'
        )
        close_btn.pack(pady=10)
