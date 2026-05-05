from tkinter import *
from tkinter import ttk, messagebox
import random
import time
from sorting_algorithms import *
from complexity_analyzer import ComplexityAnalyzer

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title('🎯 Advanced Sorting Algorithm Visualizer')
        self.root.geometry("1200x800")
        self.root.config(bg='#1e1e2e')
        
        # Variables
        self.arr = []
        self.select_algorithm = StringVar()
        self.is_sorting = False
        
        # Color scheme
        self.colors = {
            'bg': '#1e1e2e',
            'frame_bg': '#2d2d44',
            'canvas_bg': '#3d3d5c',
            'primary': '#89b4fa',
            'secondary': '#f38ba8',
            'success': '#a6e3a1',
            'warning': '#fab387',
            'accent': '#cba6f7',
            'text': '#cdd6f4',
            'bar_default': '#89b4fa',
            'bar_comparing': '#f9e2af',
            'bar_sorted': '#a6e3a1'
        }
        
        # Initialize UI
        self.create_widgets()
        self.complexity_analyzer = ComplexityAnalyzer()
        
    def create_widgets(self):
        # Title Frame
        title_frame = Frame(self.root, bg=self.colors['bg'], height=60)
        title_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        
        title_label = Label(
            title_frame, 
            text="🎯 Sorting Algorithm Visualizer", 
            font=('Helvetica', 24, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        title_label.pack(pady=10)
        
        # Control Panel Frame
        self.control_frame = Frame(
            self.root, 
            bg=self.colors['frame_bg'], 
            relief=RIDGE, 
            bd=3
        )
        self.control_frame.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        
        # Canvas Frame
        self.canvas_frame = Frame(
            self.root, 
            bg=self.colors['frame_bg'],
            relief=RIDGE,
            bd=3
        )
        self.canvas_frame.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        
        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)
        
        # Create control panel widgets
        self.create_control_panel()
        
        # Create canvas
        self.create_canvas()
        
    def create_control_panel(self):
        # Algorithm Selection
        Label(
            self.control_frame, 
            text="Select Algorithm",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        ).grid(row=0, column=0, padx=15, pady=15, sticky='w')
        
        algorithms = [
            'Bubble Sort', 
            'Selection Sort', 
            'Insertion Sort',
            'Merge Sort',
            'Quick Sort',
            'Heap Sort'
        ]
        
        self.algo_menu = ttk.Combobox(
            self.control_frame,
            textvariable=self.select_algorithm,
            values=algorithms,
            state='readonly',
            font=('Helvetica', 11),
            width=18
        )
        self.algo_menu.grid(row=0, column=1, padx=15, pady=15, sticky='ew')
        self.algo_menu.current(0)
        self.algo_menu.bind('<<ComboboxSelected>>', self.show_complexity)
        
        # Sorting Speed
        Label(
            self.control_frame,
            text="Sorting Speed",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        ).grid(row=1, column=0, padx=15, pady=10, sticky='w')
        
        self.speed_scale = Scale(
            self.control_frame,
            from_=0.01,
            to=1.0,
            resolution=0.01,
            orient=HORIZONTAL,
            length=200,
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            highlightbackground=self.colors['primary'],
            troughcolor=self.colors['canvas_bg'],
            activebackground=self.colors['primary']
        )
        self.speed_scale.set(0.1)
        self.speed_scale.grid(row=1, column=1, padx=15, pady=10, sticky='ew')
        
        # Array Size
        Label(
            self.control_frame,
            text="Array Size",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        ).grid(row=2, column=0, padx=15, pady=10, sticky='w')
        
        self.size_scale = Scale(
            self.control_frame,
            from_=5,
            to=100,
            resolution=1,
            orient=HORIZONTAL,
            length=200,
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            highlightbackground=self.colors['success'],
            troughcolor=self.colors['canvas_bg'],
            activebackground=self.colors['success']
        )
        self.size_scale.set(30)
        self.size_scale.grid(row=2, column=1, padx=15, pady=10, sticky='ew')
        
        # Min Value
        Label(
            self.control_frame,
            text="Min Value",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        ).grid(row=3, column=0, padx=15, pady=10, sticky='w')
        
        self.min_scale = Scale(
            self.control_frame,
            from_=1,
            to=50,
            resolution=1,
            orient=HORIZONTAL,
            length=200,
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            highlightbackground=self.colors['warning'],
            troughcolor=self.colors['canvas_bg'],
            activebackground=self.colors['warning']
        )
        self.min_scale.set(10)
        self.min_scale.grid(row=3, column=1, padx=15, pady=10, sticky='ew')
        
        # Max Value
        Label(
            self.control_frame,
            text="Max Value",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        ).grid(row=4, column=0, padx=15, pady=10, sticky='w')
        
        self.max_scale = Scale(
            self.control_frame,
            from_=50,
            to=200,
            resolution=1,
            orient=HORIZONTAL,
            length=200,
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            highlightbackground=self.colors['secondary'],
            troughcolor=self.colors['canvas_bg'],
            activebackground=self.colors['secondary']
        )
        self.max_scale.set(100)
        self.max_scale.grid(row=4, column=1, padx=15, pady=10, sticky='ew')
        
        # Buttons Frame
        button_frame = Frame(self.control_frame, bg=self.colors['frame_bg'])
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Generate Array Button
        self.generate_btn = Button(
            button_frame,
            text="🔄 Generate Array",
            command=self.generate_array,
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['accent'],
            relief=RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.generate_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # Start Sorting Button
        self.sort_btn = Button(
            button_frame,
            text="▶ Start Sorting",
            command=self.start_sorting,
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            activebackground='#86d993',
            relief=RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.sort_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Analyze Complexity Button
        self.analyze_btn = Button(
            button_frame,
            text="📊 Analyze Complexity",
            command=self.analyze_complexity,
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            activebackground='#d4a3f9',
            relief=RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.analyze_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
        # Complexity Info Frame
        self.info_frame = Frame(
            self.control_frame,
            bg=self.colors['canvas_bg'],
            relief=SUNKEN,
            bd=2
        )
        self.info_frame.grid(row=6, column=0, columnspan=2, padx=15, pady=20, sticky='ew')
        
        Label(
            self.info_frame,
            text="Time Complexity",
            font=('Helvetica', 11, 'bold'),
            bg=self.colors['canvas_bg'],
            fg=self.colors['primary']
        ).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Complexity labels
        self.best_label = Label(
            self.info_frame,
            text="Best: -",
            font=('Helvetica', 10),
            bg=self.colors['canvas_bg'],
            fg=self.colors['success']
        )
        self.best_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        
        self.avg_label = Label(
            self.info_frame,
            text="Average: -",
            font=('Helvetica', 10),
            bg=self.colors['canvas_bg'],
            fg=self.colors['warning']
        )
        self.avg_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        
        self.worst_label = Label(
            self.info_frame,
            text="Worst: -",
            font=('Helvetica', 10),
            bg=self.colors['canvas_bg'],
            fg=self.colors['secondary']
        )
        self.worst_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
        
        self.space_label = Label(
            self.info_frame,
            text="Space: -",
            font=('Helvetica', 10),
            bg=self.colors['canvas_bg'],
            fg=self.colors['accent']
        )
        self.space_label.grid(row=4, column=0, padx=10, pady=5, sticky='w')
        
        # Show initial complexity
        self.show_complexity()
        
    def create_canvas(self):
        canvas_title = Label(
            self.canvas_frame,
            text="Visualization Area",
            font=('Helvetica', 14, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        )
        canvas_title.pack(pady=10)
        
        self.canvas = Canvas(
            self.canvas_frame,
            bg=self.colors['canvas_bg'],
            highlightthickness=2,
            highlightbackground=self.colors['primary']
        )
        self.canvas.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Stats label
        self.stats_label = Label(
            self.canvas_frame,
            text="Comparisons: 0 | Swaps: 0 | Time: 0.00s",
            font=('Helvetica', 11),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        )
        self.stats_label.pack(pady=10)
        
    def generate_array(self):
        if self.is_sorting:
            messagebox.showwarning("Warning", "Please wait for sorting to complete!")
            return
            
        size = int(self.size_scale.get())
        min_val = int(self.min_scale.get())
        max_val = int(self.max_scale.get())
        
        if min_val >= max_val:
            messagebox.showerror("Error", "Min value must be less than Max value!")
            return
        
        self.arr = [random.randint(min_val, max_val) for _ in range(size)]
        self.draw_array(self.arr, [self.colors['bar_default']] * len(self.arr))
        self.stats_label.config(text="Array Generated! Ready to sort.")
        
    def draw_array(self, arr, color_array):
        self.canvas.delete("all")
        canvas_height = self.canvas.winfo_height() - 40
        canvas_width = self.canvas.winfo_width() - 20
        
        if canvas_height <= 0 or canvas_width <= 0:
            canvas_height = 600
            canvas_width = 800
        
        if len(arr) == 0:
            return
            
        bar_width = canvas_width / (len(arr) + 1)
        offset = 10
        spacing = 2
        
        max_val = max(arr) if arr else 1
        normalized_arr = [i / max_val for i in arr]
        
        for i, height in enumerate(normalized_arr):
            x0 = i * bar_width + offset + spacing
            y0 = canvas_height - height * (canvas_height - 40)
            x1 = (i + 1) * bar_width + offset
            y1 = canvas_height
            
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=color_array[i],
                outline='white',
                width=1
            )
            
            # Show value on top if array is small
            if len(arr) <= 50:
                self.canvas.create_text(
                    x0 + (bar_width - spacing) / 2,
                    y0 - 5,
                    text=str(arr[i]),
                    font=('Helvetica', 8),
                    fill='white'
                )
        
        self.root.update_idletasks()
        
    def start_sorting(self):
        if self.is_sorting:
            messagebox.showwarning("Warning", "Sorting already in progress!")
            return
            
        if not self.arr:
            messagebox.showwarning("Warning", "Please generate an array first!")
            return
        
        self.is_sorting = True
        self.sort_btn.config(state=DISABLED, bg='grey')
        self.generate_btn.config(state=DISABLED, bg='grey')
        
        algorithm = self.select_algorithm.get()
        speed = self.speed_scale.get()
        
        start_time = time.time()
        comparisons = [0]
        swaps = [0]
        
        try:
            if algorithm == 'Bubble Sort':
                bubble_sort(self.arr, self.draw_array, speed, comparisons, swaps, self.colors)
            elif algorithm == 'Selection Sort':
                selection_sort(self.arr, self.draw_array, speed, comparisons, swaps, self.colors)
            elif algorithm == 'Insertion Sort':
                insertion_sort(self.arr, self.draw_array, speed, comparisons, swaps, self.colors)
            elif algorithm == 'Merge Sort':
                merge_sort(self.arr, 0, len(self.arr) - 1, self.draw_array, speed, comparisons, swaps, self.colors)
            elif algorithm == 'Quick Sort':
                quick_sort(self.arr, 0, len(self.arr) - 1, self.draw_array, speed, comparisons, swaps, self.colors)
            elif algorithm == 'Heap Sort':
                heap_sort(self.arr, self.draw_array, speed, comparisons, swaps, self.colors)
            
            end_time = time.time()
            elapsed = end_time - start_time
            
            # Final sorted visualization
            self.draw_array(self.arr, [self.colors['bar_sorted']] * len(self.arr))
            
            self.stats_label.config(
                text=f"✓ Sorted! | Comparisons: {comparisons[0]} | Swaps: {swaps[0]} | Time: {elapsed:.2f}s"
            )
            
            messagebox.showinfo("Success", f"Sorting completed!\n\nComparisons: {comparisons[0]}\nSwaps: {swaps[0]}\nTime: {elapsed:.2f}s")
            
        except Exception as e:
            messagebox.showerror("Error", f"Sorting error: {str(e)}")
        
        finally:
            self.is_sorting = False
            self.sort_btn.config(state=NORMAL, bg=self.colors['success'])
            self.generate_btn.config(state=NORMAL, bg=self.colors['primary'])
    
    def show_complexity(self, event=None):
        algorithm = self.select_algorithm.get()
        complexities = {
            'Bubble Sort': ('O(n)', 'O(n²)', 'O(n²)', 'O(1)'),
            'Selection Sort': ('O(n²)', 'O(n²)', 'O(n²)', 'O(1)'),
            'Insertion Sort': ('O(n)', 'O(n²)', 'O(n²)', 'O(1)'),
            'Merge Sort': ('O(n log n)', 'O(n log n)', 'O(n log n)', 'O(n)'),
            'Quick Sort': ('O(n log n)', 'O(n log n)', 'O(n²)', 'O(log n)'),
            'Heap Sort': ('O(n log n)', 'O(n log n)', 'O(n log n)', 'O(1)')
        }
        
        if algorithm in complexities:
            best, avg, worst, space = complexities[algorithm]
            self.best_label.config(text=f"Best: {best}")
            self.avg_label.config(text=f"Average: {avg}")
            self.worst_label.config(text=f"Worst: {worst}")
            self.space_label.config(text=f"Space: {space}")
    
    def analyze_complexity(self):
        algorithm = self.select_algorithm.get()
        self.complexity_analyzer.analyze_and_plot(algorithm)


def main():
    root = Tk()
    app = SortingVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
