import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext, filedialog
import webbrowser
import requests
from urllib.parse import urljoin, urlparse
import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import shutil
import zipfile
import re

# Check for required packages
try:
    import whois  # pip install python-whois
except ImportError:
    messagebox.showwarning("Missing Module", "Install 'python-whois' using: pip install python-whois")

try:
    from bs4 import BeautifulSoup  # pip install beautifulsoup4
except ImportError:
    messagebox.showwarning("Missing Module", "Install 'beautifulsoup4' using: pip install beautifulsoup4")


class DarkBossTools:
    def __init__(self, root):
        self.root = root
        self.root.title("💀 DARKBOSS1BD - ALL IN ONE HACKING TOOL 💀")
        self.root.geometry("950x750")
        self.root.resizable(False, False)
        self.root.configure(bg="#0e0e0e")

        # Fonts
        self.title_font = ("Consolas", 16, "bold")
        self.tool_font = ("Courier", 10, "bold")
        self.link_font = ("Helvetica", 10, "underline")

        # --- Banner ---
        banner = tk.Label(
            self.root,
            text="DARKBOSS1BD",
            font=("Courier", 28, "bold"),
            fg="#00ff00",
            bg="#000000",
            relief="solid",
            bd=2
        )
        banner.pack(fill="x", pady=5)

        # --- Hacker Animation ---
        self.anim_text = scrolledtext.ScrolledText(
            self.root,
            height=8,
            bg="black",
            fg="#00ff00",
            font=("Courier", 9),
            wrap="word"
        )
        self.anim_text.pack(pady=5, padx=10, fill="x")
        self.anim_text.insert("1.0", "[+] Booting DarkBoss1BD System...\n")
        self.anim_text.config(state="disabled")

        threading.Thread(target=self.animate_boot, daemon=True).start()

        # --- Tools Frame (Grid) ---
        tools_frame = tk.Frame(self.root, bg="#111111")
        tools_frame.pack(pady=10, padx=20, fill="both", expand=True)

        tools = [
            ("🌐 Website Cloner", self.website_cloner),
            ("🔍 Web Info Tools", self.web_info_tool),
            ("⚡ Vulnerability Scanner", self.vuln_scanner),
            ("🦠 Virus URL Checker", self.virus_url_checker),
            ("📧 Email Sender", self.email_sender_tool)
        ]

        for i, (name, func) in enumerate(tools):
            btn = tk.Button(
                tools_frame,
                text=name,
                font=self.tool_font,
                bg="#1a1a1a",
                fg="#00ccff",
                width=25,
                height=2,
                relief="groove",
                command=func
            )
            btn.grid(row=i//3, column=i%3, padx=20, pady=15)

        # --- Footer Links ---
        footer = tk.Frame(self.root, bg="#0e0e0e")
        footer.pack(side="bottom", fill="x", pady=10)

        tk.Label(
            footer,
            text="📩 Telegram: @darkvaiadmin | 🌐 Website: serialkey.top",
            font=self.link_font,
            fg="#00ccff",
            bg="#0e0e0e"
        ).pack()

        telegram_link = tk.Label(footer, text="Click here to contact on Telegram", fg="cyan", bg="#0e0e0e", cursor="hand2")
        telegram_link.pack()
        telegram_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/darkvaiadmin"))

        website_link = tk.Label(footer, text="Visit our Website: serialkey.top", fg="cyan", bg="#0e0e0e", cursor="hand2")
        website_link.pack()
        website_link.bind("<Button-1>", lambda e: webbrowser.open("https://serialkey.top/"))

    def animate_boot(self):
        time.sleep(0.5)
        messages = [
            "[+] Initializing Dark System...",
            "[✓] Loading Kernel Modules...",
            "[✓] Accessing Dark Network...",
            "[✓] Bypassing Security Protocols...",
            "[✓] Fetching Tools from DarkBoss Server...",
            "[✓] All Tools Ready.\n[+] DARKBOSS1BD SYSTEM ONLINE 🔥\n"
        ]
        self.anim_text.config(state="normal")
        for msg in messages:
            self.anim_text.insert("end", msg + "\n")
            self.anim_text.see("end")
            self.anim_text.update()
            time.sleep(0.4)
        self.anim_text.config(state="disabled")

    def log(self, msg):
        if hasattr(self, 'output_text'):
            self.output_text.config(state="normal")
            self.output_text.insert("end", msg + "\n")
            self.output_text.see("end")
            self.output_text.config(state="disabled")

    # --- 1. Advanced Website Cloner with ZIP Download ---
    def website_cloner(self):
        win = tk.Toplevel(self.root)
        win.title("🌐 Website Cloner with ZIP Download")
        win.geometry("700x500")
        win.configure(bg="#111")

        tk.Label(win, text="Enter Website URL:", fg="cyan", bg="#111", font=("Helvetica", 12)).pack(pady=10)
        url_entry = tk.Entry(win, width=60, font=("Helvetica", 10))
        url_entry.pack(pady=5)
        url_entry.insert(0, "https://")

        # Output Log
        self.output_text = scrolledtext.ScrolledText(win, height=15, bg="black", fg="lime", font=("Courier", 9))
        self.output_text.pack(padx=10, pady=10, fill="both", expand=True)
        self.output_text.config(state="disabled")

        # Buttons
        button_frame = tk.Frame(win, bg="#111")
        button_frame.pack(pady=5)

        clone_btn = tk.Button(button_frame, text="Clone Website", bg="#005f5f", fg="white", width=15)
        clone_btn.grid(row=0, column=0, padx=5)

        download_btn = tk.Button(button_frame, text="Download as ZIP", bg="#00008b", fg="white", width=15, state="disabled")
        download_btn.grid(row=0, column=1, padx=5)

        # Variables
        self.cloned_folder = None

        def start_clone():
            url = url_entry.get().strip()
            if not url.startswith("http"):
                url = "https://" + url

            # Ask for save location
            folder = filedialog.askdirectory(title="Select Folder to Save Cloned Website")
            if not folder:
                return

            base = urlparse(url)
            site_name = re.sub(r'[^\w\-_\.]', '_', base.netloc)
            self.cloned_folder = os.path.join(folder, site_name)
            os.makedirs(self.cloned_folder, exist_ok=True)

            # Create subfolders
            for d in ['css', 'js', 'images', 'pages']:
                os.makedirs(os.path.join(self.cloned_folder, d), exist_ok=True)

            self.output_text.config(state="normal")
            self.output_text.delete("1.0", "end")
            self.log(f"[+] Cloning {url} into {self.cloned_folder}...")

            threading.Thread(target=self.clone_full_site, args=(url, download_btn), daemon=True).start()

        def download_zip():
            if not self.cloned_folder or not os.path.exists(self.cloned_folder):
                messagebox.showwarning("Error", "No cloned site found to zip!")
                return
            zip_path = self.cloned_folder + ".zip"
            try:
                shutil.make_archive(self.cloned_folder, 'zip', self.cloned_folder)
                self.log(f"[✓] ZIP created: {zip_path}")
                messagebox.showinfo("Success", f"Website cloned and zipped!\n📁 {zip_path}")
                webbrowser.open(os.path.dirname(zip_path))  # Open folder
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create ZIP: {str(e)}")

        clone_btn.config(command=start_clone)
        download_btn.config(command=download_zip)

        # Update button state after clone
        win.bind("<Destroy>", lambda e: download_btn.config(state="normal") if self.cloned_folder else None)

    def clone_full_site(self, url, download_btn):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Save main HTML
            main_html = os.path.join(self.cloned_folder, "index.html")
            with open(main_html, "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            self.log("[✓] Saved index.html")

            # Download CSS
            for link in soup.find_all("link", rel="stylesheet"):
                href = link.get("href")
                if not href:
                    continue
                css_url = urljoin(url, href)
                try:
                    res = requests.get(css_url, timeout=10)
                    filename = os.path.basename(urlparse(css_url).path) or f"style_{len(os.listdir(os.path.join(self.cloned_folder, 'css')))}.css"
                    filepath = os.path.join(self.cloned_folder, "css", filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(res.text)
                    link["href"] = f"css/{filename}"
                    self.log(f"[✓] CSS: {filename}")
                except Exception as e:
                    self.log(f"[!] CSS Failed: {e}")

            # Download JS
            for script in soup.find_all("script", src=True):
                js_url = urljoin(url, script["src"])
                try:
                    res = requests.get(js_url, timeout=10)
                    filename = os.path.basename(urlparse(js_url).path) or f"script_{len(os.listdir(os.path.join(self.cloned_folder, 'js')))}.js"
                    filepath = os.path.join(self.cloned_folder, "js", filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(res.text)
                    script["src"] = f"js/{filename}"
                    self.log(f"[✓] JS: {filename}")
                except Exception as e:
                    self.log(f"[!] JS Failed: {e}")

            # Download Images
            for img in soup.find_all("img", src=True):
                img_url = urljoin(url, img["src"])
                try:
                    img_data = requests.get(img_url, timeout=10).content
                    filename = os.path.basename(urlparse(img_url).path)
                    if "." not in filename:
                        filename = "image.png"
                    filepath = os.path.join(self.cloned_folder, "images", filename)
                    with open(filepath, "wb") as f:
                        f.write(img_data)
                    img["src"] = f"images/{filename}"
                    self.log(f"[✓] Image: {filename}")
                except Exception as e:
                    self.log(f"[!] Image Failed: {e}")

            # Update and save final HTML
            with open(main_html, "w", encoding="utf-8") as f:
                f.write(soup.prettify())

            self.log("[🎉] Cloning Complete! You can now download the ZIP.")
            download_btn.config(state="normal")

        except Exception as e:
            self.log(f"[❌] Error: {str(e)}")

    # --- 2. Web Info Tools (Unchanged) ---
    def web_info_tool(self):
        win = tk.Toplevel(self.root)
        win.title("🔍 Web Info Tool")
        win.geometry("600x400")
        win.configure(bg="#111")
        tk.Label(win, text="Enter Website URL:", fg="cyan", bg="#111", font=("Helvetica", 12)).pack(pady=10)
        url_entry = tk.Entry(win, width=50, font=("Helvetica", 10))
        url_entry.pack(pady=5)
        self.output_text = scrolledtext.ScrolledText(win, height=15, bg="black", fg="lime", font=("Courier", 9))
        self.output_text.pack(padx=10, pady=10, fill="both", expand=True)
        self.output_text.config(state="disabled")

        def fetch_info():
            url = url_entry.get().strip()
            if not url.startswith("http"):
                url = "https://" + url
            try:
                parsed = urlparse(url)
                domain = parsed.netloc
                self.log(f"[+] Fetching info for: {domain}")
                response = requests.get(url, timeout=10)
                self.log(f"Status Code: {response.status_code}")
                self.log(f"Server: {response.headers.get('Server', 'Unknown')}")
                self.log(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
                self.log(f"Content-Length: {len(response.content)} bytes")
                try:
                    import whois
                    w = whois.whois(domain)
                    self.log(f"WHOIS: Registrar={w.registrar}, Expires={w.expiration_date}")
                except:
                    self.log("WHOIS: Failed to fetch (install python-whois)")
            except Exception as e:
                self.log(f"[!] Error: {str(e)}")
        tk.Button(win, text="Fetch Info", bg="#005f5f", fg="white", command=fetch_info).pack(pady=5)

    # --- 3. Vulnerability Scanner (Unchanged) ---
    def vuln_scanner(self):
        win = tk.Toplevel(self.root)
        win.title("⚡ Vulnerability Scanner")
        win.geometry("600x400")
        win.configure(bg="#111")
        tk.Label(win, text="Enter Website URL:", fg="cyan", bg="#111", font=("Helvetica", 12)).pack(pady=10)
        url_entry = tk.Entry(win, width=50, font=("Helvetica", 10))
        url_entry.pack(pady=5)
        self.output_text = scrolledtext.ScrolledText(win, height=15, bg="black", fg="lime", font=("Courier", 9))
        self.output_text.pack(padx=10, pady=10, fill="both", expand=True)
        self.output_text.config(state="disabled")

        def scan():
            url = url_entry.get().strip()
            if not url.startswith("http"):
                url = "https://" + url
            payloads = [url + "'", url + "/../../../../etc/passwd", url + "<script>alert(1)</script>"]
            self.log(f"[+] Scanning {url}...\n")
            for p in payloads:
                try:
                    r = requests.get(p, timeout=5)
                    if "sql" in r.text.lower() or r.status_code == 500:
                        self.log(f"[⚠️] Possible SQLi: {p}")
                    elif "root:" in r.text:
                        self.log(f"[⚠️] LFI: {p}")
                    elif "<script>alert(1)</script>" in r.text:
                        self.log(f"[⚠️] XSS: {p}")
                    else:
                        self.log(f"[✓] Safe: {p}")
                except:
                    self.log(f"[!] Failed: {p}")
        tk.Button(win, text="Scan Vulnerabilities", bg="#5f0000", fg="white", command=scan).pack(pady=5)

    # --- 4. Virus URL Checker (Unchanged) ---
    def virus_url_checker(self):
        win = tk.Toplevel(self.root)
        win.title("🦠 Virus URL Checker")
        win.geometry("600x400")
        win.configure(bg="#111")
        tk.Label(win, text="Enter URL to Check:", fg="cyan", bg="#111", font=("Helvetica", 12)).pack(pady=10)
        url_entry = tk.Entry(win, width=50, font=("Helvetica", 10))
        url_entry.pack(pady=5)
        self.output_text = scrolledtext.ScrolledText(win, height=15, bg="black", fg="lime", font=("Courier", 9))
        self.output_text.pack(padx=10, pady=10, fill="both", expand=True)
        self.output_text.config(state="disabled")

        def check_url():
            url = url_entry.get().strip()
            suspicious = ["admin", "login", "phish", "malware", "bit.ly", "tinyurl"]
            if any(kw in url for kw in suspicious):
                self.log(f"[🔴] Suspicious: {', '.join([kw for kw in suspicious if kw in url])}")
            else:
                self.log(f"[🟢] Seems safe: {url}")
            self.log("\nNote: Use VirusTotal API for real scan.")
        tk.Button(win, text="Check URL", bg="#5f005f", fg="white", command=check_url).pack(pady=5)

    # --- 5. Email Sender Tool (Unchanged) ---
    def email_sender_tool(self):
        win = tk.Toplevel(self.root)
        win.title("📧 Email Sender Tool")
        win.geometry("600x500")
        win.configure(bg="#111")
        fields = [("Sender Email", "sender_email"), ("App Password", "app_password"),
                  ("Recipient Email", "recipient"), ("Subject", "subject")]
        entries = {}
        for i, (lbl, key) in enumerate(fields):
            tk.Label(win, text=lbl + ":", fg="cyan", bg="#111").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(win, width=40, show="*" if key == "app_password" else "")
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[key] = entry
        tk.Label(win, text="Message:", fg="cyan", bg="#111").grid(row=4, column=0, padx=10, pady=5, sticky="nw")
        message_text = tk.Text(win, height=8, width=40, bg="black", fg="white")
        message_text.grid(row=4, column=1, padx=10, pady=5)
        self.output_text = scrolledtext.ScrolledText(win, height=6, bg="black", fg="lime", font=("Courier", 9))
        self.output_text.pack(padx=10, pady=10, fill="x")
        self.output_text.config(state="disabled")

        def send_email():
            s = entries["sender_email"].get()
            p = entries["app_password"].get()
            r = entries["recipient"].get()
            sub = entries["subject"].get()
            body = message_text.get("1.0", "end-1c")
            if not all([s, p, r, sub, body]):
                self.log("[!] All fields required!")
                return
            try:
                msg = MIMEMultipart()
                msg["From"] = s
                msg["To"] = r
                msg["Subject"] = sub
                msg.attach(MIMEText(body, "plain"))
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(s, p)
                server.sendmail(s, r, msg.as_string())
                server.quit()
                self.log("[✓] Email sent!")
            except Exception as e:
                self.log(f"[!] Failed: {str(e)}")
        tk.Button(win, text="Send Email", bg="#005f00", fg="white", command=send_email).pack(pady=10)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = DarkBossTools(root)
    root.mainloop()
