import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("1000x700")

        # Background Gradient
        self.create_gradient_background()

        # Header
        header = tk.Frame(self.root, bg="#4CAF50", height=80)
        header.pack(fill="x")

        logo = tk.Label(header, text="🌟", font=("Arial", 30, "bold"), bg="#4CAF50", fg="white")
        logo.pack(side="left", padx=10, pady=10)

        title = tk.Label(header, text="Admin Dashboard", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white")
        title.pack(side="left", padx=10)

        # Table Frame
        self.table_frame = tk.Frame(self.root, bd=2, relief="solid", bg="white")
        self.table_frame.place(x=50, y=120, width=900, height=400)

        # Scrollbars for the Table
        scroll_x = ttk.Scrollbar(self.table_frame, orient="horizontal")
        scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical")

        # User Table
        self.user_table = ttk.Treeview(
            self.table_frame,
            columns=("email", "fname", "lname", "role", "status"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            show="headings"
        )
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")

        scroll_x.config(command=self.user_table.xview)
        scroll_y.config(command=self.user_table.yview)

        # Table Headings
        self.user_table.heading("email", text="Email")
        self.user_table.heading("fname", text="First Name")
        self.user_table.heading("lname", text="Last Name")
        self.user_table.heading("role", text="Role")
        self.user_table.heading("status", text="Status")

        self.user_table.column("email", width=200, anchor="center")
        self.user_table.column("fname", width=150, anchor="center")
        self.user_table.column("lname", width=150, anchor="center")
        self.user_table.column("role", width=100, anchor="center")
        self.user_table.column("status", width=100, anchor="center")

        self.user_table.pack(fill="both", expand=True)

        # Add Alternating Row Colors
        self.user_table.tag_configure("oddrow", background="white")
        self.user_table.tag_configure("evenrow", background="#f9f9f9")

        self.user_table.bind("<ButtonRelease-1>", self.select_user)

        # Button Frame
        self.button_frame = tk.Frame(self.root, bg="white")
        self.button_frame.place(x=50, y=550, width=900, height=100)

        # Approve Button
        self.create_stylish_button(
            self.button_frame, "Approve", self.approve_user, x=50, bg="#4CAF50", hover_bg="#45a049"
        )

        # Decline Button
        self.create_stylish_button(
            self.button_frame, "Decline", self.decline_user, x=350, bg="#757575", hover_bg="#616161"
        )

        # Delete Button
        self.create_stylish_button(
            self.button_frame, "Delete", self.delete_user, x=650, bg="#f44336", hover_bg="#e53935"
        )

        # Load Users
        self.load_users()

    def create_gradient_background(self):
        canvas = tk.Canvas(self.root, width=1000, height=700, highlightthickness=0)
        canvas.place(x=0, y=0)

        # Create a vertical gradient
        start_color = "#D3CCE3"
        end_color = "#E9E4F0"
        steps = 256  # Number of steps for the gradient
        for i in range(steps):
            # Calculate the color for each step
            r1, g1, b1 = self.hex_to_rgb(start_color)
            r2, g2, b2 = self.hex_to_rgb(end_color)
            r = int(r1 + (r2 - r1) * i / steps)
            g = int(g1 + (g2 - g1) * i / steps)
            b = int(b1 + (b2 - b1) * i / steps)
            color = f"#{r:02x}{g:02x}{b:02x}"

            # Draw a line for each step
            y = int((700 / steps) * i)  # Map the step to canvas height
            canvas.create_line(0, y, 1000, y, fill=color)

# Utility function to convert hex color to RGB
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
   
   
    def create_stylish_button(self, parent, text, command, x, bg, hover_bg):
        button = tk.Button(
            parent, text=text, command=command,
            font=("Arial", 14, "bold"),
            bg=bg, fg="white", width=12, height=2, relief="flat"
        )
        button.place(x=x, y=20)

        button.bind("<Enter>", lambda e: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.config(bg=bg))

    def connect_db(self):
        return mysql.connector.connect(
            host="localhost", username="root", password="admin@2309", database="fras"
        )

    def load_users(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT email, fname, lname, role, status FROM register WHERE email != 'admin@gmail.com'")
            rows = cursor.fetchall()
            self.user_table.delete(*self.user_table.get_children())

            for index, row in enumerate(rows):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.user_table.insert("", "end", values=row, tags=(tag,))

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading users: {e}")

    def select_user(self, event):
        selected_item = self.user_table.focus()
        self.selected_row = self.user_table.item(selected_item, "values")

    def approve_user(self):
        self.update_user_status("approve", "approved")

    def decline_user(self):
        self.update_user_status("decline", "declined")

    def delete_user(self):
        if not hasattr(self, "selected_row") or not self.selected_row:
            messagebox.showwarning("Warning", "Please select a user first.")
            return

        try:
            email = self.selected_row[0]
            if email == "admin@gmail.com":
                messagebox.showerror("Error", "You cannot delete the admin account.")
                return

            confirm = messagebox.askyesno("Confirmation", f"Are you sure you want to delete the user {email}?")
            if confirm:
                conn = self.connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM register WHERE email = %s", (email,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"User {email} has been deleted.")
                self.load_users()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting user: {e}")

    def update_user_status(self, status, action):
        if not hasattr(self, "selected_row") or not self.selected_row:
            messagebox.showwarning("Warning", "Please select a user first.")
            return

        try:
            email = self.selected_row[0]
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE register SET status = %s WHERE email = %s", (status, email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"User {email} has been {action}.")
            self.load_users()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating user: {e}")


# Run the Admin Dashboard
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()
