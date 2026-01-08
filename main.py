import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import os

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x500")
        self.root.resizable(False, False)


        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12, "bold"))


        ttk.Label(root, text="Video URL:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)


        ttk.Label(root, text="Timestamps (optional):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.timestamps_entry = ttk.Entry(root, width=50)
        self.timestamps_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        ttk.Label(root, text="Format: *00:00:00-00:00:00 (for video clips)").grid(row=2, column=1, padx=10, pady=5, sticky="w")


        self.download_button = ttk.Button(root, text="Download", command=self.start_download)
        self.download_button.grid(row=3, column=1, padx=10, pady=20)


        self.output_text = scrolledtext.ScrolledText(root, width=70, height=15, font=("Courier", 10))
        self.output_text.grid(row=4, column=0, padx=10, pady=10, columnspan=3)
        self.output_text.config(state=tk.DISABLED)


        self.status_label = ttk.Label(root, text="Ready", foreground="blue")
        self.status_label.grid(row=5, column=0, padx=10, pady=5, columnspan=3)

    def start_download(self):
        url = self.url_entry.get().strip()
        timestamps = self.timestamps_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return

        self.download_button.config(state=tk.DISABLED)
        self.status_label.config(text="Downloading...", foreground="orange")
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)

        threading.Thread(target=self.download_video, args=(url, timestamps)).start()

    def download_video(self, url, timestamps):
        try:
            if timestamps:

                command = [
                    "yt-dlp",
                    "--download-sections",
                    f"*{timestamps}",
                    "-f",
                    "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/best[height<=1080]",
                    url
                ]
            else:

                command = [
                    "yt-dlp",
                    "-f",
                    "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/best[height<=1080]",
                    url
                ]


            result = subprocess.run(command, capture_output=True, text=True, cwd=os.getcwd())


            self.root.after(0, self.update_output, result.stdout, result.stderr, result.returncode)

        except Exception as e:
            self.root.after(0, self.update_output, "", str(e), 1)

    def update_output(self, stdout, stderr, returncode):
        self.output_text.config(state=tk.NORMAL)
        if stdout:
            self.output_text.insert(tk.END, stdout)
        if stderr:
            self.output_text.insert(tk.END, stderr)
        self.output_text.config(state=tk.DISABLED)

        if returncode == 0:
            self.status_label.config(text="Download completed successfully!", foreground="green")
        else:
            self.status_label.config(text="Download failed. Check output for details.", foreground="red")

        self.download_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
