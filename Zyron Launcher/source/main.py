import customtkinter as ctk
import threading
import random
from launcher import launch_zyron_offline

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class ZyronLauncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Zyron Launcher")
        
        # Fullscreen setup
        self.attributes("-fullscreen", True)
        self.configure(fg_color="#100c19") 
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        # --- ANIMATED FALLING WHITE DOTS (SNOW EFFECT) ---
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, bg="#100c19")
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.num_dots = 65
        self.dots = []
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()

        for _ in range(self.num_dots):
            x = random.randint(0, w)
            y = random.randint(0, h)
            speed = random.uniform(1.2, 3.5)
            size = random.randint(2, 5)
            dot_id = self.canvas.create_oval(x, y, x + size, y + size, fill="#ffffff", outline="")
            self.dots.append({"id": dot_id, "x": x, "y": y, "speed": speed, "size": size})

        self.animate_snow()

        # --- CENTER CONTAINER FRAME ---
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # --- HEADER (Top Middle) ---
        self.title_label = ctk.CTkLabel(
            self.center_frame, 
            text="ZYRON CLIENT", 
            font=ctk.CTkFont(family="Helvetica", size=38, weight="bold"),
            text_color="#c4b5fd"
        )
        self.title_label.pack(pady=(0, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.center_frame, 
            text="Next-Generation Custom Minecraft Experience", 
            font=ctk.CTkFont(size=14),
            text_color="#9ca3af"
        )
        self.subtitle_label.pack(pady=(0, 25))

        # --- ACCOUNT PROFILE DISPLAY BOX ---
        self.account_frame = ctk.CTkFrame(
            self.center_frame, 
            fg_color="#1a1426", 
            corner_radius=22, 
            border_color="#7c3aed", 
            border_width=2
        )
        self.account_frame.pack(pady=10, fill="x", ipadx=30, ipady=12)

        self.account_name_label = ctk.CTkLabel(
            self.account_frame, 
            text="Not Logged In", 
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#d8b4fe"
        )
        self.account_name_label.pack(pady=(4, 0))

        self.account_email_label = ctk.CTkLabel(
            self.account_frame, 
            text="Email: None", 
            font=ctk.CTkFont(size=12),
            text_color="#9ca3af"
        )
        self.account_email_label.pack(pady=(0, 8))

        self.login_button = ctk.CTkButton(
            self.account_frame, 
            text="Log In with Account", 
            command=self.open_login_popup, 
            width=260, 
            height=40,
            corner_radius=20,
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            text_color="#ffffff",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.login_button.pack(pady=5)

        # --- VERSION SELECTION ---
        self.version_option = ctk.CTkOptionMenu(
            self.center_frame, 
            values=["26.3", "26.2", "1.21.1", "1.20.1"], 
            width=400, 
            height=48,
            corner_radius=24,
            fg_color="#4c1d95",
            button_color="#6d28d9",
            button_hover_color="#5b21b6",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.version_option.pack(pady=15)

        # --- BIG PLAY BUTTON ---
        self.launch_button = ctk.CTkButton(
            self.center_frame, 
            text="PLAY ZYRON", 
            command=self.start_launch_thread, 
            width=400, 
            height=55,
            corner_radius=28,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#7c3aed",  
            hover_color="#6d28d9", 
            text_color="#ffffff"
        )
        self.launch_button.pack(pady=(15, 10))

        # --- STATUS FOOTER ---
        self.status_label = ctk.CTkLabel(
            self.center_frame, 
            text="Ready to launch", 
            font=ctk.CTkFont(size=12),
            text_color="#9ca3af"
        )
        self.status_label.pack(pady=5)

        self.current_username = "ZyronPlayer"

    def animate_snow(self):
        h = self.winfo_screenheight()
        w = self.winfo_screenwidth()

        for dot in self.dots:
            dot["y"] += dot["speed"]
            if dot["y"] > h:
                dot["y"] = -10
                dot["x"] = random.randint(0, w)
            
            self.canvas.coords(
                dot["id"], 
                dot["x"], dot["y"], 
                dot["x"] + dot["size"], dot["y"] + dot["size"]
            )
        
        self.after(30, self.animate_snow)

    def open_login_popup(self):
        """Opens a clean popup window with Email and Password boxes."""
        popup = ctk.CTkToplevel(self)
        popup.title("Zyron Account Login")
        popup.geometry("420x350")
        popup.resizable(False, False)
        popup.configure(fg_color="#151021")
        popup.grab_set()

        popup.update_idletasks()
        x = (popup.winfo_screenwidth() - 420) // 2
        y = (popup.winfo_screenheight() - 350) // 2
        popup.geometry(f"+{x}+{y}")

        title = ctk.CTkLabel(popup, text="Sign in to Zyron Client", font=ctk.CTkFont(size=20, weight="bold"), text_color="#c4b5fd")
        title.pack(pady=(25, 15))

        email_entry = ctk.CTkEntry(
            popup, 
            placeholder_text="Email Address", 
            width=320, 
            height=42, 
            corner_radius=14, 
            fg_color="#1f1a2e", 
            border_color="#7c3aed", 
            border_width=2,
            text_color="#ffffff",
            font=ctk.CTkFont(size=13)
        )
        email_entry.pack(pady=8)

        password_entry = ctk.CTkEntry(
            popup, 
            placeholder_text="Password", 
            show="*", 
            width=320, 
            height=42, 
            corner_radius=14, 
            fg_color="#1f1a2e", 
            border_color="#7c3aed", 
            border_width=2,
            text_color="#ffffff",
            font=ctk.CTkFont(size=13)
        )
        password_entry.pack(pady=8)

        error_label = ctk.CTkLabel(popup, text="", font=ctk.CTkFont(size=11), text_color="#ef4444")
        error_label.pack(pady=2)

        def process_login():
            email_val = email_entry.get().strip()
            pass_val = password_entry.get().strip()
            
            if email_val and pass_val:
                # Extracts a clean username from the email (e.g., user@gmail.com -> USER)
                self.current_username = email_val.split("@")[0].upper()
                
                # Update main launcher interface instantly
                self.account_name_label.configure(text=f"Logged in as: {self.current_username}")
                self.account_email_label.configure(text=f"Email: {email_val}")
                self.login_button.configure(text="Switch Account", fg_color="#374151")
                
                self.status_label.configure(text=f"Successfully signed in as {self.current_username}")
                popup.destroy()
            else:
                error_label.configure(text="Please fill in both email and password.", text_color="#ef4444")

        submit_btn = ctk.CTkButton(
            popup, 
            text="Sign In", 
            command=process_login, 
            width=320, 
            height=45, 
            corner_radius=20, 
            fg_color="#7c3aed", 
            hover_color="#6d28d9", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        submit_btn.pack(pady=(15, 10))

    def start_launch_thread(self):
        threading.Thread(target=self.run_launcher, daemon=True).start()

    def run_launcher(self):
        version = self.version_option.get()
        self.status_label.configure(text=f"Preparing version {version}...")
        self.launch_button.configure(state="disabled", fg_color="#374151")

        try:
            launch_zyron_offline(self.current_username, version)
            self.status_label.configure(text="Game running...")
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}")
        finally:
            self.launch_button.configure(state="normal", fg_color="#7c3aed")
            self.status_label.configure(text="Ready to launch")

if __name__ == "__main__":
    app = ZyronLauncherApp()
    app.mainloop()