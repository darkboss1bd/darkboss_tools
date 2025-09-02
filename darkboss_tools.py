import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import os
import shutil
import zipfile
import threading
import time

# Main App
class WebsiteClonerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 DARKBOSS1BD - Advanced Website Cloner 💀")
        self.root.geometry("800x600")
        self.root.configure(bg="#0d0d0d")

        # Fonts
        title_font = ("Consolas", 18, "bold")
        btn_font = ("Courier", 12, "bold")

        # Banner
        banner = tk.Label(
            self.root,
            text="DARKBOSS1BD",
            font=("Courier", 28, "bold"),
            fg="#00ff00",
            bg="#000000",
            relief="solid",
            bd=2
        )
        banner.pack(fill="x", pady=10)

        # URL Input
        tk.Label(self.root, text="Enter Website URL (e.g., https://example.com):", fg="cyan", bg="#0d0d0d", font=("Helvetica", 12)).pack(pady=10)
        self.url_entry = tk.Entry(self.root, width=60, font=("Helvetica", 11))
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, "https://")

        # Clone Button
        clone_btn = tk.Button(
            self.root,
            text="🚀 Clone Website & Generate ZIP",
            font=btn_font,
            bg="#005f00",
            fg="white",
            command=self.start_clone
        )
        clone_btn.pack(pady=20)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=600, mode="determinate")
        self.progress.pack(pady=10)

        # Log Box
        self.log_text = tk.Text(self.root, height=20, bg="black", fg="#00ff00", font=("Courier", 9))
        self.log_text.pack(padx=20, pady=10, fill="both", expand=True)

        # Footer Links
        footer = tk.Frame(self.root, bg="#0d0d0d")
        footer.pack(side="bottom", fill="x", pady=10)

        tk.Label(footer, text="📩 Telegram: @darkvaiadmin | 🌐 Website: serialkey.top", fg="cyan", bg="#0d0d0d").pack()
        link1 = tk.Label(footer, text="Contact on Telegram", fg="lightblue", bg="#0d0d0d", cursor="hand2")
        link1.pack()
        link1.bind("<Button-1>", lambda e: open_url("https://t.me/darkvaiadmin"))
        link2 = tk.Label(footer, text="Visit Our Website", fg="lightblue", bg="#0d0d0d", cursor="hand2")
        link2.pack()
        link2.bind("<Button-1>", lambda e: open_url("https://serialkey.top/"))

    def log(self, msg):
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.root.update()

    def start_clone(self):
        url = self.url_entry.get().strip()
        if not url.startswith("http"):
            messagebox.showerror("Error", "Please enter a valid URL with http:// or https://")
            return

        # Ask for save location
        folder = filedialog.askdirectory(title="Select Folder to Save Cloned Website")
        if not folder:
            return

        self.progress["value"] = 0
        self.log_text.delete("1.0", "end")
        self.log(f"[+] Starting clone of: {url}")
        threading.Thread(target=self.clone_website, args=(url, folder), daemon=True).start()

    def clone_website(self, url, save_folder):
        try:
            base = urlparse(url)
            site_name = f"{base.netloc}"
            main_dir = os.path.join(save_folder, site_name)
            os.makedirs(main_dir, exist_ok=True)
            css_dir = os.path.join(main_dir, "css")
            js_dir = os.path.join(main_dir, "js")
            img_dir = os.path.join(main_dir, "images")
            os.makedirs(css_dir, exist_ok=True)
            os.makedirs(js_dir, exist_ok=True)
            os.makedirs(img_dir, exist_ok=True)

            self.log(f"[✓] Created directories for {site_name}")

            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Save HTML
            html_path = os.path.join(main_dir, "index.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            self.log("[✓] Saved index.html")

            # Download CSS
            css_files = soup.find_all("link", rel="stylesheet")
            for link in css_files:
                css_url = link.get("href")
                if not css_url:
                    continue
                full_css = urljoin(url, css_url)
                try:
                    res = requests.get(full_css, timeout=10)
                    filename = os.path.basename(urlparse(full_css).path) or f"style_{len(os.listdir(css_dir))}.css"
                    filepath = os.path.join(css_dir, filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(res.text)
                    link["href"] = f"css/{filename}"
                    self.log(f"[✓] Downloaded CSS: {filename}")
                except Exception as e:
                    self.log(f"[!] Failed CSS: {full_css} | {e}")

            # Download JS
            js_files = soup.find_all("script", src=True)
            for script in js_files:
                js_url = script["src"]
                full_js = urljoin(url, js_url)
                try:
                    res = requests.get(full_js, timeout=10)
                    filename = os.path.basename(urlparse(full_js).path) or f"script_{len(os.listdir(js_dir))}.js"
                    filepath = os.path.join(js_dir, filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(res.text)
                    script["src"] = f"js/{filename}"
                    self.log(f"[✓] Downloaded JS: {filename}")
                except Exception as e:
                    self.log(f"[!] Failed JS: {full_js} | {e}")

            # Download Images
            img_tags = soup.find_all("img")
            for img in img_tags:
                src = img.get("src")
                if not src:
                    continue
                img_url = urljoin(url, src)
                try:
                    img_data = requests.get(img_url, timeout=10).content
                    filename = os.path.basename(urlparse(img_url).path)
                    if "." not in filename:
                        filename = "image.png"
                    filepath = os.path.join(img_dir, filename)
                    with open(filepath, "wb") as f:
                        f.write(img_data)
                    img["src"] = f"images/{filename}"
                    self.log(f"[✓] Downloaded Image: {filename}")
                except Exception as e:
                    self.log(f"[!] Failed Image: {img_url} | {e}")

            # Update HTML with new paths
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(soup.prettify())

            self.log("[✓] HTML updated with local paths")

            # Create ZIP
            zip_path = os.path.join(save_folder, f"{site_name}.zip")
            self.log(f"[📦] Creating ZIP: {zip_path}")
            shutil.make_archive(os.path.join(save_folder, site_name), 'zip', main_dir)
            self.log(f"[✓] ZIP created: {zip_path}")

            self.progress["value"] = 100
            messagebox.showinfo("Success", f"Website cloned successfully!\nSaved at: {zip_path}")
        except Exception as e:
            self.log(f"[❌] Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to clone: {str(e)}")


def open_url(url):
    import webbrowser
    webbrowser.open(url)


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = WebsiteClonerApp(root)
    root.mainloop()