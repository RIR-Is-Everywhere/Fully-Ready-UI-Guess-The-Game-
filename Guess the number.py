import tkinter as tk
import random

class GuessTheNumberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code_RIR Guess the Number")
        self.root.geometry("1000x800")
        self.root.configure(bg="#050505")
        self.root.resizable(False, False)
        
        self.lower_bound = 1
        self.upper_bound = 20
        self.secret_number = random.randint(self.lower_bound, self.upper_bound)
        self.attempts = 0
        
        self.canvas = tk.Canvas(self.root, width=1000, height=800, bg="#050505", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.draw_cyberpunk_bg()
        self.setup_ui()
        
    def draw_cyberpunk_bg(self):
        horizon = 400
        
        # Grid glow color
        grid_color = "#004d1a" # dark neon green
        glow_grid = "#001a09"
        
        # Horizontal lines
        for i in range(1, 30):
            y = horizon + (i**2.4)
            if y > 800: break
            self.canvas.create_line(0, y-1, 1000, y-1, fill=glow_grid, width=3)
            self.canvas.create_line(0, y, 1000, y, fill=grid_color, width=1)
            
        # Perspective lines
        center_x = 500
        for i in range(-20, 21):
            if i == 0: continue
            x_bottom = center_x + i * 80
            self.canvas.create_line(center_x, horizon, x_bottom, 800, fill=glow_grid, width=3)
            self.canvas.create_line(center_x, horizon, x_bottom, 800, fill=grid_color, width=1)
            
        # Draw a horizon line (neon red/pink)
        self.canvas.create_line(0, horizon-2, 1000, horizon-2, fill="#4d0012", width=4)
        self.canvas.create_line(0, horizon, 1000, horizon, fill="#ff073a", width=2)
        
        # Adds some "stars" or particles
        for _ in range(80):
            x = random.randint(0, 1000)
            y = random.randint(0, horizon-10)
            self.canvas.create_rectangle(x, y, x+2, y+2, fill="#39ff14", outline="")
            
    def create_glowing_text(self, x, y, text, font_family, font_size, color, glow_color, tags=""):
        font_main = (font_family, font_size, "bold")
        
        # Glow layers matching Tkinter text
        offsets = [(-2,0), (2,0), (0,-2), (0,2), (-1,-1), (-1,1), (1,-1), (1,1)]
        for dx, dy in offsets:
            self.canvas.create_text(x+dx, y+dy, text=text, font=font_main, fill=glow_color, tags=f"{tags}_glow" if tags else "", justify=tk.CENTER)
            
        self.canvas.create_text(x, y, text=text, font=font_main, fill=color, tags=tags, justify=tk.CENTER)

    def setup_ui(self):
        # Title
        self.create_glowing_text(500, 80, "Guess the Number", "Courier New", 56, "#ffffff", "#39ff14", "title")
        
        # Subtitle
        self.create_glowing_text(500, 160, f"TARGET: {self.lower_bound} to {self.upper_bound}", "Courier New", 24, "#ffffff", "#ff073a", "subtitle")
        
        # Entry Frame to look like terminal input
        entry_frame = tk.Frame(self.root, bg="#39ff14", bd=2) # neon green border
        
        self.entry = tk.Entry(entry_frame, font=("Courier New", 28, "bold"), width=5, justify="center", 
                              bg="#0a0a0a", fg="#39ff14", insertbackground="#39ff14", relief=tk.FLAT)
        self.entry.pack(padx=3, pady=3)
        self.entry.bind('<Return>', lambda event: self.check_guess())
        
        self.canvas.create_window(350, 300, window=entry_frame)
        self.entry.focus()
        
        # Submit Button
        btn_frame = tk.Frame(self.root, bg="#ff073a", bd=2)
        self.submit_btn = tk.Button(btn_frame, text="EXECUTE", font=("Courier New", 22, "bold"), bg="#0a0a0a", fg="#ff073a",
                                    activebackground="#ff073a", activeforeground="#0a0a0a", relief=tk.FLAT, bd=0, 
                                    command=self.check_guess, cursor="cross")
        self.submit_btn.pack(padx=3, pady=3, ipadx=10, ipady=6)
        self.canvas.create_window(650, 300, window=btn_frame)
        
        # Feedback Text
        self.create_glowing_text(500, 480, "SYSTEM READY.\nAWAITING INPUT...", "Courier New", 26, "#ffffff", "#39ff14", "feedback")
        
        # Restart Button Frame
        self.restart_frame = tk.Frame(self.root, bg="#39ff14", bd=2)
        self.restart_btn = tk.Button(self.restart_frame, text="REBOOT SYSTEM", font=("Courier New", 20, "bold"), 
                                     bg="#0a0a0a", fg="#39ff14", activebackground="#39ff14", activeforeground="#0a0a0a", 
                                     relief=tk.FLAT, bd=0, command=self.reset_game, cursor="cross")
        self.restart_btn.pack(padx=3, pady=3, ipadx=15, ipady=8)
        self.restart_window = self.canvas.create_window(500, 650, window=self.restart_frame, state=tk.HIDDEN)
        
    def update_feedback(self, text, color, glow_color):
        self.canvas.delete("feedback")
        self.canvas.delete("feedback_glow")
        self.create_glowing_text(500, 480, text, "Courier New", 26, color, glow_color, "feedback")

    def check_guess(self):
        if str(self.submit_btn['state']) == tk.DISABLED or self.submit_btn.cget('state') == 'disabled':
            return
            
        try:
            user_guess = int(self.entry.get())
            self.attempts += 1
            
            if user_guess == self.secret_number:
                self.update_feedback(f"ACCESS GRANTED!\nTarget {self.secret_number} breached in {self.attempts} cycles.", "#ffffff", "#39ff14")
                self.submit_btn.config(state=tk.DISABLED)
                self.entry.config(state=tk.DISABLED)
                self.canvas.itemconfigure(self.restart_window, state=tk.NORMAL)
            elif user_guess < self.secret_number:
                self.update_feedback("ERR: Value Too Low.\nIncrease coordinates.", "#ffffff", "#ff073a")
            else:
                self.update_feedback("ERR: Value Too High.\nDecrease coordinates.", "#ffffff", "#ff073a")
                
            self.entry.delete(0, tk.END)
        except ValueError:
            self.update_feedback("FATAL: Invalid Data Type.\nNumbers only.", "#ffffff", "#ff073a")
            self.entry.delete(0, tk.END)
            
    def reset_game(self):
        self.secret_number = random.randint(self.lower_bound, self.upper_bound)
        self.attempts = 0
        self.update_feedback("SYSTEM REBOOTED.\nAWAITING INPUT...", "#ffffff", "#39ff14")
        self.submit_btn.config(state=tk.NORMAL)
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.canvas.itemconfigure(self.restart_window, state=tk.HIDDEN)
        self.entry.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = GuessTheNumberApp(root)
    root.mainloop()