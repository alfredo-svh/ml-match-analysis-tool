import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.colorchooser import askcolor

from main import hex_to_rgb, run_processing


class MatchAnalysisApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Football Analysis Tool")
        self.root.geometry("850x650")
        self.root.minsize(650, 500)

        # Track colors (Hex values)
        self.colors = {
            "team1_player": "#3498db",
            "team1_gk": "#2ecc71",
            "team2_player": "#e74c3c",
            "team2_gk": "#f1c40f",
        }

        self.selected_file_path = ""
        self.create_widgets()

    def create_widgets(self):
        # --- File Selector Section ---
        file_frame = ttk.LabelFrame(self.root, text=" File Selection ", padding=10)
        file_frame.pack(fill="x", padx=15, pady=10)

        self.file_label = ttk.Label(
            file_frame, text="No file selected", foreground="gray"
        )
        self.file_label.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_browse = ttk.Button(
            file_frame, text="Browse...", command=self.browse_file
        )
        btn_browse.pack(side="right")

        # --- Home Team Section ---
        set1_frame = ttk.LabelFrame(self.root, text=" Home Team ", padding=10)
        set1_frame.pack(fill="x", padx=15, pady=5)

        self.btn_s1_c1 = tk.Button(
            set1_frame,
            text="Player Color",
            bg=self.colors["team1_player"],
            command=lambda: self.pick_color("team1_player", self.btn_s1_c1),
            width=10,
        )
        self.btn_s1_c1.grid(row=0, column=0, padx=5, pady=5)

        self.btn_s1_c2 = tk.Button(
            set1_frame,
            text="Goalkeeper Color",
            bg=self.colors["team1_gk"],
            command=lambda: self.pick_color("team1_gk", self.btn_s1_c2),
            width=10,
        )
        self.btn_s1_c2.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(set1_frame, text="Team Name:").grid(
            row=0, column=2, padx=(10, 5), sticky="w"
        )
        self.entry_set1 = ttk.Entry(set1_frame)
        self.entry_set1.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        set1_frame.columnconfigure(3, weight=1)

        btn_s1_save = ttk.Button(
            set1_frame, text="Save Team", command=lambda: self.save_team_config(1)
        )
        btn_s1_save.grid(row=0, column=4, padx=5, pady=5)

        btn_s1_load = ttk.Button(
            set1_frame, text="Load Team", command=lambda: self.load_team_config(1)
        )
        btn_s1_load.grid(row=0, column=5, padx=5, pady=5)

        # --- Away Team Section ---
        set2_frame = ttk.LabelFrame(self.root, text=" Away Team ", padding=10)
        set2_frame.pack(fill="x", padx=15, pady=5)

        self.btn_s2_c1 = tk.Button(
            set2_frame,
            text="Player Color",
            bg=self.colors["team2_player"],
            command=lambda: self.pick_color("team2_player", self.btn_s2_c1),
            width=10,
        )
        self.btn_s2_c1.grid(row=0, column=0, padx=5, pady=5)

        self.btn_s2_c2 = tk.Button(
            set2_frame,
            text="Goalkeeper Color",
            bg=self.colors["team2_gk"],
            command=lambda: self.pick_color("team2_gk", self.btn_s2_c2),
            width=10,
        )
        self.btn_s2_c2.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(set2_frame, text="Team Name:").grid(
            row=0, column=2, padx=(10, 5), sticky="w"
        )
        self.entry_set2 = ttk.Entry(set2_frame)
        self.entry_set2.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        set2_frame.columnconfigure(3, weight=1)

        btn_s2_save = ttk.Button(
            set2_frame, text="Save Team", command=lambda: self.save_team_config(2)
        )
        btn_s2_save.grid(row=0, column=4, padx=5, pady=5)

        btn_s2_load = ttk.Button(
            set2_frame, text="Load Team", command=lambda: self.load_team_config(2)
        )
        btn_s2_load.grid(row=0, column=5, padx=5, pady=5)

        # --- Action Button ---
        self.btn_process = ttk.Button(
            self.root, text="Process Data", command=self.process_data, state="disabled"
        )
        self.btn_process.pack(pady=15)

    # --- Widget Logic / Event Handlers ---

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("All Files", "*.*")],
        )
        if file_path:
            self.selected_file_path = file_path
            # Truncate view if path is too long
            display_path = (
                f"...{file_path[-40:]}" if len(file_path) > 40 else file_path
            )
            self.file_label.config(text=display_path, foreground="black")

            self.btn_process.config(state="normal")

    def pick_color(self, color_key, button_widget):
        # Open standard Tkinter color picker
        current_color = self.colors[color_key]
        color_code = askcolor(color=current_color, title="Choose Color")[1]
        if color_code:
            self.colors[color_key] = color_code
            button_widget.config(bg=color_code)

    def save_team_config(self, team_num):
        """Saves a single team's name and color configurations to a JSON file."""
        if team_num == 1:
            team_data = {
                "name": self.entry_set1.get(),
                "player_color": self.colors["team1_player"],
                "gk_color": self.colors["team1_gk"],
            }
        else:
            team_data = {
                "name": self.entry_set2.get(),
                "player_color": self.colors["team2_player"],
                "gk_color": self.colors["team2_gk"],
            }

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title=f"Save Team {team_num} Configuration",
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    json.dump(team_data, f, indent=4)
                messagebox.showinfo("Success", f"Team {team_num} preset saved!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save preset: {e}")

    def load_team_config(self, team_num):
        """Loads a single team's configuration and updates only that team's widgets."""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")],
            title=f"Load Team {team_num} Configuration",
        )

        if file_path:
            try:
                with open(file_path, "r") as f:
                    team_data = json.load(f)

                if team_num == 1:
                    # Update internal dictionary
                    self.colors["team1_player"] = team_data.get("player_color", self.colors["team1_player"])
                    self.colors["team1_gk"] = team_data.get("gk_color", self.colors["team1_gk"])
                    
                    # Update entry field
                    self.entry_set1.delete(0, tk.END)
                    self.entry_set1.insert(0, team_data.get("name", ""))
                    
                    # Update button colors
                    self.btn_s1_c1.config(bg=self.colors["team1_player"])
                    self.btn_s1_c2.config(bg=self.colors["team1_gk"])
                else:
                    # Update internal dictionary
                    self.colors["team2_player"] = team_data.get("player_color", self.colors["team2_player"])
                    self.colors["team2_gk"] = team_data.get("gk_color", self.colors["team2_gk"])
                    
                    # Update entry field
                    self.entry_set2.delete(0, tk.END)
                    self.entry_set2.insert(0, team_data.get("name", ""))
                    
                    # Update button colors
                    self.btn_s2_c1.config(bg=self.colors["team2_player"])
                    self.btn_s2_c2.config(bg=self.colors["team2_gk"])

                messagebox.showinfo("Success", f"Team {team_num} preset loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load preset: {e}")

    def process_data(self):
        if not self.selected_file_path:
            return
        
        self.btn_process.config(state="disabled")
        
        home_team = self.entry_set1.get()
        away_team = self.entry_set2.get()
        home_player_color = hex_to_rgb(self.colors["team1_player"])
        home_gk_color = hex_to_rgb(self.colors["team1_gk"])
        away_player_color = hex_to_rgb(self.colors["team2_player"])
        away_gk_color = hex_to_rgb(self.colors["team2_gk"])

        try:
            run_processing(
                self.selected_file_path,
                home_team,
                home_player_color,
                home_gk_color,
                away_team,
                away_player_color,
                away_gk_color,
            )
        except Exception as e:
            print(f"ERROR: {e}")



if __name__ == "__main__":
    root = tk.Tk()
    app = MatchAnalysisApp(root)
    root.mainloop()