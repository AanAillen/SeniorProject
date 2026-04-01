#!/usr/bin/env python3
"""
Fisheye Correction GUI

A simple popup application that allows a user to select a video file and run
the barrel distortion correction script (`fix_barrel.py`) on it.

Usage:
    python3 codeFiles/gui_app.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import os
import sys

# Ensure we are in the project root if the script is run directly from the codeFiles dir
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

class VideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fisheye Distortion Correction") 
        self.root.geometry("500x350")
        self.root.configure(padx=20, pady=20)
        
        self.selected_file_path = None
        
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="Fisheye Distortion Correction", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # Instructions
        instruction_label = tk.Label(self.root, text="1. Upload a video to correct the fisheye distortion\n2. Click run to execute the correction'", justify=tk.LEFT)
        instruction_label.pack(anchor="w", pady=(0, 10))

        # File Selection Frame
        file_frame = tk.Frame(self.root)
        file_frame.pack(fill=tk.X, pady=(0, 20))

        self.select_btn = tk.Button(file_frame, text="Select Video", command=self.select_file)
        self.select_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.file_label = tk.Label(file_frame, text="No file selected", fg="gray", wraplength=350, justify=tk.LEFT)
        self.file_label.pack(side=tk.LEFT, fill=tk.X)

        # Action Button Frame
        action_frame = tk.Frame(self.root)
        action_frame.pack(fill=tk.X, pady=(10, 20))

        self.run_btn = tk.Button(action_frame, text="Run", command=self.run_script, state=tk.DISABLED, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.run_btn.pack(side=tk.LEFT)

        # Status and Progress
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, fg="blue")
        self.status_label.pack(anchor="w")

        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=460, mode='indeterminate')
        
    def select_file(self):
        filetypes = (
            ('Video files', '*.mp4 *.avi *.mov *.mkv'),
            ('All files', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='Open a video file',
            initialdir=project_root,
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file_path = filename
            # Just show the filename, not the full path to keep UI clean
            short_name = os.path.basename(filename)
            self.file_label.config(text=f".../{short_name}", fg="black")
            self.run_btn.config(state=tk.NORMAL)
            self.status_var.set("Video loaded. Ready to run.")

    def run_script(self):
        if not self.selected_file_path:
            messagebox.showerror("Error", "Please select a video file first.")
            return

        # Disable UI during processing
        self.select_btn.config(state=tk.DISABLED)
        self.run_btn.config(state=tk.DISABLED)
        self.status_var.set(f"Processing '{os.path.basename(self.selected_file_path)}'...")
        self.progress.pack(pady=(10, 0))
        self.progress.start(10)
        
        # Determine paths
        script_path = os.path.join(current_dir, "fix_barrel.py")
        
        # Run in a separate thread so GUI doesn't freeze
        thread = threading.Thread(target=self.execute_process, args=(script_path, self.selected_file_path))
        thread.daemon = True
        thread.start()

    def execute_process(self, script, input_video):
        try:
            # We use subprocess.run, piping the output.
            # fix_barrel.py prints progress with \r, which is hard to parse live from subprocess
            # without complex unbuffered reads. So we just wait for it to finish.
            
            # Using python3 explicitly
            result = subprocess.run(
                [sys.executable, script, input_video], 
                cwd=project_root, 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                self.root.after(0, self.processing_complete, True, "Processing completed successfuly!")
            else:
                error_msg = f"Script failed with error:\n{result.stderr[-200:] if result.stderr else 'Unknown error'}"
                self.root.after(0, self.processing_complete, False, error_msg)
                
        except Exception as e:
            self.root.after(0, self.processing_complete, False, str(e))

    def processing_complete(self, success, message):
        # Stop progress bar
        self.progress.stop()
        self.progress.pack_forget()
        
        # Re-enable UI
        self.select_btn.config(state=tk.NORMAL)
        self.run_btn.config(state=tk.NORMAL)
        
        if success:
            self.status_var.set("Done. Check the 'processed_videos' folder.")
            self.status_label.config(fg="green")
            messagebox.showinfo("Success", "Video processed successfully!\nThe output is in the 'processed_videos' directory.")
        else:
            self.status_var.set("Error occurred during processing.")
            self.status_label.config(fg="red")
            messagebox.showerror("Error", f"Failed to process video.\n\n{message}")


if __name__ == "__main__":
    root = tk.Tk()
    
    # Try to make it look a bit more modern on Mac
    try:
        from tkinter import ttk
        style = ttk.Style()
        if 'aqua' in style.theme_names():
            style.theme_use('aqua')
    except:
        pass
        
    app = VideoProcessorApp(root)
    root.mainloop()
