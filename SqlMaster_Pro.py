import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime

# ==========================================
#  SQL MASTER PRO - ONE FILE PROJECT
# ==========================================

class SQLMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Master Pro - Query Generator")
        self.root.geometry("800x600")
        
        # --- Theme & Styles ---
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colors
        self.bg_color = "#f4f6f9"
        self.sidebar_color = "#2c3e50"
        self.accent_color = "#3498db"
        self.text_color = "#2c3e50"
        
        self.root.configure(bg=self.bg_color)
        
        # Define Custom Styles
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=5)
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#2c3e50")
        
        # --- Data Storage ---
        self.query_history = []

        # --- Main Layout ---
        self.create_layout()

    def create_layout(self):
        # 1. Main Container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 2. Notebook (Tabs)
        self.tabs = ttk.Notebook(main_container)
        self.tabs.pack(fill="both", expand=True)

        # --- Tab 1: Basic Builder (CRUD) ---
        self.tab_basic = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_basic, text="  🛠 Basic Builder  ")
        self.build_basic_tab()

        # --- Tab 2: Join Builder ---
        self.tab_join = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_join, text="  🔗 Join Builder  ")
        self.build_join_tab()

        # --- Tab 3: History ---
        self.tab_history = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_history, text="  📜 History  ")
        self.build_history_tab()
        
        # --- Footer ---
        footer = tk.Label(self.root, text="SQL Master Pro v1.0 | Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#e0e0e0")
        footer.pack(side=tk.BOTTOM, fill=tk.X)

    # ==========================================
    #  TAB 1: BASIC BUILDER LOGIC
    # ==========================================
    def build_basic_tab(self):
        frame = ttk.Frame(self.tab_basic)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Row 0: Operation Selection
        lbl_op = ttk.Label(frame, text="Operation Type:")
        lbl_op.grid(row=0, column=0, sticky="w", pady=5)
        
        self.var_operation = tk.StringVar(value="SELECT")
        self.cb_operation = ttk.Combobox(frame, textvariable=self.var_operation, state="readonly", 
                                         values=["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE TABLE"])
        self.cb_operation.grid(row=0, column=1, sticky="ew", pady=5)
        self.cb_operation.bind("<<ComboboxSelected>>", self.update_basic_ui)

        # Row 1: Table Name
        ttk.Label(frame, text="Table Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_table = ttk.Entry(frame)
        self.entry_table.grid(row=1, column=1, sticky="ew", pady=5)

        # Row 2: Field 1 (Dynamic Label)
        self.lbl_field1 = ttk.Label(frame, text="Columns:")
        self.lbl_field1.grid(row=2, column=0, sticky="w", pady=5)
        self.entry_field1 = ttk.Entry(frame)
        self.entry_field1.insert(0, "*")
        self.entry_field1.grid(row=2, column=1, sticky="ew", pady=5)

        # Row 3: Field 2 (Dynamic Label)
        self.lbl_field2 = ttk.Label(frame, text="Conditions (WHERE):")
        self.lbl_field2.grid(row=3, column=0, sticky="w", pady=5)
        self.entry_field2 = ttk.Entry(frame)
        self.entry_field2.grid(row=3, column=1, sticky="ew", pady=5)

        # Row 4: Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=1, sticky="e", pady=15)
        
        btn_gen = tk.Button(btn_frame, text="Generate SQL", bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), command=self.generate_basic_sql)
        btn_gen.pack(side=tk.LEFT, padx=5)
        
        btn_copy = tk.Button(btn_frame, text="Copy to Clipboard", bg="#3498db", fg="white", font=("Segoe UI", 10), command=lambda: self.copy_to_clipboard(self.txt_output_basic))
        btn_copy.pack(side=tk.LEFT, padx=5)

        # Row 5: Output
        ttk.Label(frame, text="Generated SQL:").grid(row=5, column=0, sticky="nw", pady=5)
        self.txt_output_basic = scrolledtext.ScrolledText(frame, height=8, font=("Consolas", 10))
        self.txt_output_basic.grid(row=6, column=0, columnspan=2, sticky="nsew")

        frame.columnconfigure(1, weight=1)

    def update_basic_ui(self, event=None):
        op = self.var_operation.get()
        if op == "SELECT":
            self.lbl_field1.config(text="Columns (comma sep):")
            self.lbl_field2.config(text="WHERE Clause:")
            self.entry_field1.delete(0, tk.END); self.entry_field1.insert(0, "*")
        elif op == "INSERT":
            self.lbl_field1.config(text="Columns (comma sep):")
            self.lbl_field2.config(text="Values (comma sep):")
            self.entry_field1.delete(0, tk.END)
        elif op == "UPDATE":
            self.lbl_field1.config(text="SET (col=val):")
            self.lbl_field2.config(text="WHERE Clause:")
            self.entry_field1.delete(0, tk.END)
        elif op == "DELETE":
            self.lbl_field1.config(text="(Leave Empty)")
            self.lbl_field2.config(text="WHERE Clause:")
            self.entry_field1.delete(0, tk.END)
        elif op == "CREATE TABLE":
            self.lbl_field1.config(text="Column Definitions:")
            self.lbl_field2.config(text="(Leave Empty)")
            self.entry_field1.delete(0, tk.END); self.entry_field1.insert(0, "id INT, name VARCHAR(50)")

    def generate_basic_sql(self):
        op = self.var_operation.get()
        table = self.entry_table.get().strip()
        f1 = self.entry_field1.get().strip()
        f2 = self.entry_field2.get().strip()

        if not table:
            messagebox.showerror("Error", "Table Name is required!")
            return

        sql = ""
        if op == "SELECT":
            sql = f"SELECT {f1} FROM {table}"
            if f2: sql += f"\nWHERE {f2}"
        elif op == "INSERT":
            sql = f"INSERT INTO {table} ({f1})\nVALUES ({f2})"
        elif op == "UPDATE":
            sql = f"UPDATE {table}\nSET {f1}"
            if f2: sql += f"\nWHERE {f2}"
        elif op == "DELETE":
            sql = f"DELETE FROM {table}"
            if f2: sql += f"\nWHERE {f2}"
        elif op == "CREATE TABLE":
            sql = f"CREATE TABLE {table} (\n    {f1}\n)"
        
        sql += ";"
        self.display_result(self.txt_output_basic, sql)
        self.add_to_history(sql)

    # ==========================================
    #  TAB 2: JOIN BUILDER LOGIC
    # ==========================================
    def build_join_tab(self):
        frame = ttk.Frame(self.tab_join)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Table A
        grp_a = ttk.LabelFrame(frame, text="Table A (Left)")
        grp_a.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.ent_join_a = ttk.Entry(grp_a); self.ent_join_a.pack(fill="x", padx=5, pady=5)
        
        # Table B
        grp_b = ttk.LabelFrame(frame, text="Table B (Right)")
        grp_b.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.ent_join_b = ttk.Entry(grp_b); self.ent_join_b.pack(fill="x", padx=5, pady=5)

        # Join Condition
        ttk.Label(frame, text="ON Condition (e.g. A.id = B.user_id):").grid(row=1, column=0, columnspan=2, sticky="w", pady=(10,5))
        self.ent_join_on = ttk.Entry(frame)
        self.ent_join_on.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Join Type
        ttk.Label(frame, text="Join Type:").grid(row=3, column=0, sticky="w", pady=5)
        self.cb_join_type = ttk.Combobox(frame, values=["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"], state="readonly")
        self.cb_join_type.current(0)
        self.cb_join_type.grid(row=3, column=1, sticky="ew", pady=5)

        # Generate Button
        btn_gen = tk.Button(frame, text="Generate Join Query", bg="#8e44ad", fg="white", font=("Segoe UI", 10, "bold"), command=self.generate_join_sql)
        btn_gen.grid(row=4, column=0, columnspan=2, pady=15)

        # Output
        self.txt_output_join = scrolledtext.ScrolledText(frame, height=8, font=("Consolas", 10))
        self.txt_output_join.grid(row=5, column=0, columnspan=2, sticky="nsew")
        
        frame.columnconfigure(0, weight=1); frame.columnconfigure(1, weight=1)

    def generate_join_sql(self):
        ta = self.ent_join_a.get().strip()
        tb = self.ent_join_b.get().strip()
        on_cond = self.ent_join_on.get().strip()
        j_type = self.cb_join_type.get()

        if not ta or not tb or not on_cond:
            messagebox.showerror("Error", "Please fill in both tables and the ON condition.")
            return

        # Simple aliasing logic
        alias_a = ta[0] if ta else "a"
        alias_b = tb[0] if tb else "b"

        sql = f"SELECT {alias_a}.*, {alias_b}.*\nFROM {ta} {alias_a}\n{j_type} {tb} {alias_b} ON {on_cond};"
        self.display_result(self.txt_output_join, sql)
        self.add_to_history(sql)

    # ==========================================
    #  TAB 3: HISTORY LOGIC
    # ==========================================
    def build_history_tab(self):
        frame = ttk.Frame(self.tab_history)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.list_history = tk.Listbox(frame, font=("Consolas", 10), bg="#fcfcfc")
        self.list_history.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.list_history.yview)
        scrollbar.pack(side="right", fill="y")
        self.list_history.config(yscrollcommand=scrollbar.set)

        self.list_history.bind('<Double-1>', self.copy_history_to_clipboard)

    def add_to_history(self, sql):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {sql.replace(chr(10), ' ')}" # Remove newlines for listbox
        self.query_history.append(sql)
        self.list_history.insert(0, entry) # Add to top

    def copy_history_to_clipboard(self, event):
        selection = self.list_history.curselection()
        if selection:
            index = selection[0]
            # Since we insert at 0, the listbox index matches the reverse of our list
            # But simpler: just grab the text from the listbox (minus timestamp)
            full_text = self.list_history.get(index)
            # Basic extraction, or just use the list logic if kept perfectly synced
            # Let's clean the timestamp for copy
            clean_sql = full_text.split("] ", 1)[1]
            self.root.clipboard_clear()
            self.root.clipboard_append(clean_sql)
            messagebox.showinfo("Copied", "Query copied to clipboard!")

    # ==========================================
    #  UTILITIES
    # ==========================================
    def display_result(self, text_widget, content):
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, content)

    def copy_to_clipboard(self, text_widget):
        content = text_widget.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Success", "SQL copied to clipboard!")
        else:
            messagebox.showwarning("Empty", "Nothing to copy.")

# ==========================================
#  APP ENTRY POINT
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = SQLMasterApp(root)
    root.mainloop()