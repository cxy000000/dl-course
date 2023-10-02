from utils import WalkingRouteGUI
import tkinter as tk
    
if __name__ == "__main__":
    api_key = '1c5a6f863e2b10154c7ec8357f11f740' 
    
    root = tk.Tk()
    app = WalkingRouteGUI(root, api_key)
    root.mainloop()
