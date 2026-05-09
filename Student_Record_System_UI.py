import tkinter as tk
from tkinter import font, messagebox, ttk
import json
import os

class StudentRecordSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record System")
        self.root.geometry("500x700")
        self.root.configure(bg="#EBEBEB")
        
        self.student_db_file = "students.json"
        self.grade_db_file = "grades.json"

        # --- Font Configuration ---
        self.title_font = font.Font(family="Arial Black", size=22, weight="bold")
        self.button_font = font.Font(family="Arial Black", size=12, weight="bold")
        self.label_font = font.Font(family="Arial Black", size=16, weight="bold")
        self.table_header_font = font.Font(family="Arial Black", size=9, weight="bold")

        self.root.config(highlightbackground="black", highlightthickness=3)

        # --- Frames ---
        self.dashboard_frame = tk.Frame(self.root, bg="#EBEBEB")
        self.add_student_frame = tk.Frame(self.root, bg="#EBEBEB")
        self.grades_frame = tk.Frame(self.root, bg="#EBEBEB")
        self.view_records_frame = tk.Frame(self.root, bg="#EBEBEB")
        self.update_records_frame = tk.Frame(self.root, bg="#EBEBEB")
        self.delete_records_frame = tk.Frame(self.root, bg="#EBEBEB")


        self.create_dashboard()
        self.create_add_student_form()
        self.create_grades_form()
        self.create_view_all_records()
        self.create_update_record_screen()
        self.create_delete_record_screen()

        self.show_dashboard()

    def show_frame(self, frame_to_show):
        self.dashboard_frame.pack_forget()
        self.add_student_frame.pack_forget()
        self.grades_frame.pack_forget()
        self.view_records_frame.pack_forget()
        self.update_records_frame.pack_forget()
        self.delete_records_frame.pack_forget()
        frame_to_show.pack(fill="both", expand=True)

    def _read_json(self, filename):
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return []

    def _write_json(self, filename, data):
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not save data: {e}")
            return False

    # ========================================================
    # Screen 1: Dashboard/Main Menu
    # ========================================================
    def create_dashboard(self):
        header_frame = tk.Frame(self.dashboard_frame, bg="#EBEBEB", pady=20)
        header_frame.pack()
        tk.Label(header_frame, text="STUDENT RECORD", font=self.title_font, bg="#EBEBEB").pack()
        tk.Label(header_frame, text="SYSTEM", font=self.title_font, bg="#EBEBEB").pack()

        buttons = [
            ("ADD STUDENT", self.show_add_student_form),
            ("GRADES PER SUBJECT", self.show_grades_form),
            ("VIEW ALL RECORDS", self.show_view_all_records),
            ("SEARCH/UPDATE\nSTUDENT RECORD", self.show_update_record),
            ("DELETE STUDENT\nRECORD", self.show_delete_record)
        ]

        for btn_text, command_func in buttons:
            btn = tk.Button(self.dashboard_frame, text=btn_text, font=self.button_font,
                            bg="#3498DB", fg="black", relief="raised", borderwidth=2,
                            pady=10, command=command_func)
            btn.pack(pady=8, padx=60, fill='x')

    def show_dashboard(self):
        self.show_frame(self.dashboard_frame)

    # ========================================================
    # Screen 2: Add Student Form 
    # ========================================================
    def create_add_student_form(self):
        content_frame = tk.Frame(self.add_student_frame, bg="#EBEBEB", padx=30, pady=30)
        content_frame.pack(fill="both", expand=True)

        def create_form_field(parent, label_text):
            tk.Label(parent, text=label_text, font=self.label_font, bg="#EBEBEB", anchor="w").pack(fill="x", pady=(10, 5))
            entry = tk.Entry(parent, font=("Arial", 16), relief="solid", borderwidth=1)
            entry.pack(fill="x", ipady=15, pady=(0, 10))
            return entry

        self.add_ent_name = create_form_field(content_frame, "STUDENT NAME:")
        self.add_ent_id = create_form_field(content_frame, "STUDENT ID:")
        self.add_ent_program = create_form_field(content_frame, "PROGRAM:")

        actions_frame = tk.Frame(content_frame, bg="#EBEBEB")
        actions_frame.pack(side="bottom", fill="x", pady=20)
        
        tk.Button(actions_frame, text="SAVE", font=self.button_font, bg="#82A991", command=self.save_student_to_json).pack(side="right")
        tk.Button(actions_frame, text="BACK", font=self.button_font, bg="#82A991", command=self.show_dashboard).pack(side="right", padx=(5, 40))

    def show_add_student_form(self):
        self.add_ent_name.delete(0, tk.END)
        self.add_ent_id.delete(0, tk.END)
        self.add_ent_program.delete(0, tk.END)
        self.show_frame(self.add_student_frame)

    def save_student_to_json(self):
        name, sid, prog = self.add_ent_name.get().strip(), self.add_ent_id.get().strip(), self.add_ent_program.get().strip()
        if not name or not sid or not prog:
            messagebox.showwarning("Input Error", "Fill all fields!")
            return
        data = self._read_json(self.student_db_file)
        data.append({"name": name, "id": sid, "program": prog})
        if self._write_json(self.student_db_file, data):
            messagebox.showinfo("Success", "Saved!")
            self.show_dashboard()

    # ======================================================
    # Screen 3: Grades Per Subject Form 
    # ======================================================
    def create_grades_form(self):
        container = tk.Frame(self.grades_frame, bg="#EBEBEB", padx=20, pady=20)
        container.pack(fill="both", expand=True)

        # Search Bar Area (Student ID)
        search_frame = tk.Frame(container, bg="white", highlightbackground="black", highlightthickness=2)
        search_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(search_frame, text="🔍 | STUDENT ID:", font=self.table_header_font, bg="white").pack(side="left", padx=10, pady=10)
        self.grade_search_entry = tk.Entry(search_frame, font=("Arial", 14), bd=0)
        self.grade_search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Button para i-trigger ang paghahanap ng pangalan
        tk.Button(search_frame, text="FIND", command=self.find_student_for_grades).pack(side="right", padx=5)

        # Student Name Display
        self.display_name_var = tk.StringVar(value="STUDENT NAME: ")
        tk.Label(container, textvariable=self.display_name_var, font=self.label_font, bg="#EBEBEB", anchor="w").pack(fill="x", pady=10)

        # Table Header
        header_table = tk.Frame(container, bg="#EBEBEB")
        header_table.pack(fill="x")
        tk.Label(header_table, text="SUBJECTS", font=self.label_font, bg="#EBEBEB").pack(side="left", padx=40)
        tk.Label(header_table, text="GRADES", font=self.label_font, bg="#EBEBEB").pack(side="right", padx=40)

        # 8x2 Grid for Subjects and Grades
        self.grade_entries = []
        table_frame = tk.Frame(container, bg="black") # Black bg para magmukhang borders
        table_frame.pack(fill="x", pady=5)

        for r in range(8):
            sub_entry = tk.Entry(table_frame, font=("Arial", 12), relief="flat")
            sub_entry.grid(row=r, column=0, sticky="nsew", padx=1, pady=1, ipady=8)
            
            grade_entry = tk.Entry(table_frame, font=("Arial", 12), relief="flat", width=10)
            grade_entry.grid(row=r, column=1, sticky="nsew", padx=1, pady=1, ipady=8)
            
            self.grade_entries.append((sub_entry, grade_entry))

        table_frame.grid_columnconfigure(0, weight=3)
        table_frame.grid_columnconfigure(1, weight=1)

        # Buttons
        btns_frame = tk.Frame(container, bg="#EBEBEB")
        btns_frame.pack(side="bottom", fill="x", pady=20)
        
        tk.Button(btns_frame, text="SAVE", font=self.button_font, bg="#82A991", width=10, command=self.save_grades).pack(side="right", padx=5)
        tk.Button(btns_frame, text="BACK", font=self.button_font, bg="#82A991", width=10, command=self.show_dashboard).pack(side="right", padx=5)

    def show_grades_form(self):
        self.grade_search_entry.delete(0, tk.END)
        self.display_name_var.set("STUDENT NAME: ")
        for s, g in self.grade_entries:
            s.delete(0, tk.END)
            g.delete(0, tk.END)
        self.show_frame(self.grades_frame)

    def find_student_for_grades(self):
        sid = self.grade_search_entry.get().strip()
        students = self._read_json(self.student_db_file)
        # Hanapin ang student sa JSON file
        student = next((s for s in students if s['id'] == sid), None)
        
        if student:
            self.display_name_var.set(f"STUDENT NAME: {student['name'].upper()}")
        else:
            messagebox.showerror("Error", "Student ID not found!")

    def save_grades(self):
        sid = self.grade_search_entry.get().strip()
        if "STUDENT NAME: " == self.display_name_var.get() or not sid:
            messagebox.showwarning("Error", "Search for a valid Student ID first!")
            return

        grade_data = []
        for s_ent, g_ent in self.grade_entries:
            subj = s_ent.get().strip()
            grd = g_ent.get().strip()
            if subj and grd:
                grade_data.append({"subject": subj, "grade": grd})

        if not grade_data:
            messagebox.showwarning("Error", "Please enter at least one subject and grade!")
            return

        # I-save sa grades.json
        all_grades = self._read_json(self.grade_db_file)
        # Update kung existing na, o add kung bago
        updated = False
        for entry in all_grades:
            if entry['id'] == sid:
                entry['grades'] = grade_data
                updated = True
                break
        
        if not updated:
            all_grades.append({"id": sid, "grades": grade_data})

        if self._write_json(self.grade_db_file, all_grades):
            messagebox.showinfo("Success", "Grades saved successfully!")
            self.show_dashboard()

    # ======================================================
    # Screen 4: View All Receord format
    # ======================================================
    def create_view_all_records(self):
        container = tk.Frame(self.view_records_frame, bg="#EBEBEB", padx=10, pady=20)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="LIST OF STUDENTS", font=self.title_font, bg="#EBEBEB").pack(pady=(0, 20))

        # Styling para sa Table (Treeview)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", fieldbackground="white", rowheight=30, font=("Arial", 10))
        style.configure("Treeview.Heading", font=self.table_header_font, background="#D3D3D3")

        # Table Columns
        columns = ("id", "name", "program", "average", "remarks")
        self.tree = ttk.Treeview(container, columns=columns, show='headings')

        # Headings setup
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="NAME")
        self.tree.heading("program", text="PROGRAM")
        self.tree.heading("average", text="AVERAGE")
        self.tree.heading("remarks", text="REMARKS")

        # Column widths
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("program", width=100, anchor="center")
        self.tree.column("average", width=80, anchor="center")
        self.tree.column("remarks", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # OK Button
        btn_frame = tk.Frame(container, bg="#EBEBEB")
        btn_frame.pack(fill="x", pady=20)
        
        tk.Button(btn_frame, text="OK", font=self.button_font, bg="white", 
                  relief="raised", borderwidth=3, width=12, command=self.show_dashboard).pack(side="right", padx=20)

    def show_view_all_records(self):
        # Linisin ang table bago i-load ang data
        for item in self.tree.get_children():
            self.tree.delete(item)

        students = self._read_json(self.student_db_file)
        grades_list = self._read_json(self.grade_db_file)

        for s in students:
            # Hanapin ang grades ng estudyante base sa ID
            student_grades = next((g['grades'] for g in grades_list if g['id'] == s['id']), None)
            
            avg_text = "N/A"
            remarks = "N/A"

            if student_grades:
                try:
                    # Kunin ang numeric values ng grades
                    total = sum(float(g['grade']) for g in student_grades)
                    avg = total / len(student_grades)
                    avg_text = f"{avg:.2f}"
                    # Logic para sa Remarks (Halimbawa: Passing is 75)
                    remarks = "PASSED" if avg >= 75 else "FAILED"
                except:
                    avg_text = "Error"
                    remarks = "Error"

            self.tree.insert("", tk.END, values=(s['id'], s['name'].upper(), s['program'].upper(), avg_text, remarks))

        self.show_frame(self.view_records_frame)

    # ======================================================
    # Screen 5: Search/Upadate Student Record format
    # ======================================================
    def create_update_record_screen(self):
        self.update_records_frame = tk.Frame(self.root, bg="#EBEBEB")
        container = tk.Frame(self.update_records_frame, bg="#EBEBEB", padx=20, pady=10)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="UPDATE STUDENTS RECORD", font=self.table_header_font, bg="#EBEBEB").pack(pady=5)

        # Search Bar Area
        search_frame = tk.Frame(container, bg="white", highlightbackground="black", highlightthickness=2)
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(search_frame, text="🔍 | STUDENT ID:", font=self.table_header_font, bg="white").pack(side="left", padx=10, pady=10)
        self.update_search_ent = tk.Entry(search_frame, font=("Arial", 14), bd=0)
        self.update_search_ent.pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(search_frame, text="FIND", command=self.load_student_data_for_update).pack(side="right", padx=5)

        # Editable Info Fields
        tk.Label(container, text="STUDENT NAME:", font=self.table_header_font, bg="#EBEBEB", anchor="w").pack(fill="x")
        self.upd_name_ent = tk.Entry(container, font=("Arial", 12))
        self.upd_name_ent.pack(fill="x", pady=(0, 10))

        tk.Label(container, text="PROGRAM:", font=self.table_header_font, bg="#EBEBEB", anchor="w").pack(fill="x")
        self.upd_prog_ent = tk.Entry(container, font=("Arial", 12))
        self.upd_prog_ent.pack(fill="x", pady=(0, 10))

        # Table for Grades
        tk.Label(container, text="SUBJECTS                    GRADES", font=self.table_header_font, bg="#EBEBEB").pack(pady=5)
        
        self.upd_grade_entries = []
        table_frame = tk.Frame(container, bg="black")
        table_frame.pack(fill="x")

        for r in range(8):
            s_ent = tk.Entry(table_frame, font=("Arial", 10), relief="flat")
            s_ent.grid(row=r, column=0, sticky="nsew", padx=1, pady=1, ipady=5)
            g_ent = tk.Entry(table_frame, font=("Arial", 10), relief="flat", width=8)
            g_ent.grid(row=r, column=1, sticky="nsew", padx=1, pady=1, ipady=5)
            self.upd_grade_entries.append((s_ent, g_ent))
        
        table_frame.grid_columnconfigure(0, weight=3)
        table_frame.grid_columnconfigure(1, weight=1)

        # Save Button
        tk.Button(container, text="SAVE", font=self.button_font, bg="#82A991", 
                  command=self.save_updated_data).pack(side="right", pady=15)
        tk.Button(container, text="BACK", font=self.button_font, bg="#82A991", 
                  command=self.show_dashboard).pack(side="right", pady=15, padx=10)

    def show_update_record(self):
        # I-initialize ang frame kung hindi pa nagagawa
        if not hasattr(self, 'update_records_frame'):
            self.create_update_record_screen()
        
        # Clear fields
        self.update_search_ent.delete(0, tk.END)
        self.upd_name_ent.delete(0, tk.END)
        self.upd_prog_ent.delete(0, tk.END)
        for s, g in self.upd_grade_entries:
            s.delete(0, tk.END)
            g.delete(0, tk.END)
            
        self.dashboard_frame.pack_forget()
        self.add_student_frame.pack_forget()
        self.grades_frame.pack_forget()
        self.view_records_frame.pack_forget()
        self.update_records_frame.pack(fill="both", expand=True)

    def load_student_data_for_update(self):
        sid = self.update_search_ent.get().strip()
        students = self._read_json(self.student_db_file)
        grades_list = self._read_json(self.grade_db_file)

        student = next((s for s in students if s['id'] == sid), None)
        if not student:
            messagebox.showerror("Error", "Student ID not found!")
            return

        # Load Name and Program
        self.upd_name_ent.delete(0, tk.END)
        self.upd_name_ent.insert(0, student['name'])
        self.upd_prog_ent.delete(0, tk.END)
        self.upd_prog_ent.insert(0, student['program'])

        # Load Grades
        for s, g in self.upd_grade_entries:
            s.delete(0, tk.END)
            g.delete(0, tk.END)

        student_grades = next((g['grades'] for g in grades_list if g['id'] == sid), [])
        for i, entry in enumerate(student_grades):
            if i < 8:
                self.upd_grade_entries[i][0].insert(0, entry['subject'])
                self.upd_grade_entries[i][1].insert(0, entry['grade'])

    def save_updated_data(self):
        sid = self.update_search_ent.get().strip()
        new_name = self.upd_name_ent.get().strip()
        new_prog = self.upd_prog_ent.get().strip()

        if not sid or not new_name:
            messagebox.showwarning("Warning", "Name and ID cannot be empty!")
            return

        # 1. Update Students Info
        students = self._read_json(self.student_db_file)
        for s in students:
            if s['id'] == sid:
                s['name'] = new_name
                s['program'] = new_prog
                break
        self._write_json(self.student_db_file, students)

        # 2. Update Grades Info
        new_grades = []
        for s_ent, g_ent in self.upd_grade_entries:
            subj = s_ent.get().strip()
            grd = g_ent.get().strip()
            if subj and grd:
                new_grades.append({"subject": subj, "grade": grd})

        grades_list = self._read_json(self.grade_db_file)
        updated_grades = False
        for g in grades_list:
            if g['id'] == sid:
                g['grades'] = new_grades
                updated_grades = True
                break
        if not updated_grades:
            grades_list.append({"id": sid, "grades": new_grades})
        
        self._write_json(self.grade_db_file, grades_list)
        
        messagebox.showinfo("Success", "Record updated successfully!")
        self.show_dashboard()

    # ======================================================
    # Screen 6: Delete Student Record format
    # ======================================================
    def create_delete_record_screen(self):
        self.delete_records_frame = tk.Frame(self.root, bg="#EBEBEB")
        container = tk.Frame(self.delete_records_frame, bg="#EBEBEB", padx=30, pady=20)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="SELECT STUDENT YOU WANT\nTO DELETE:", 
                 font=self.label_font, bg="#EBEBEB", justify="left").pack(pady=(10, 20), anchor="w")

        # Listbox para sa mga pangalan ng estudyante
        list_frame = tk.Frame(container, bg="white", highlightbackground="black", highlightthickness=2)
        list_frame.pack(fill="both", expand=True)

        self.student_listbox = tk.Listbox(list_frame, font=("Arial", 14), bd=0, 
                                          selectbackground="#3498DB", highlightthickness=0)
        self.student_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Scrollbar para sa Listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        self.student_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.student_listbox.yview)

        # Buttons Area
        btn_frame = tk.Frame(container, bg="#EBEBEB")
        btn_frame.pack(fill="x", pady=20)

        tk.Button(btn_frame, text="DELETE", font=self.button_font, bg="white", 
                  relief="raised", borderwidth=3, width=10, command=self.delete_selected_student).pack(side="right")
        
        tk.Button(btn_frame, text="BACK", font=self.button_font, bg="white", 
                  relief="raised", borderwidth=3, width=10, command=self.show_dashboard).pack(side="right", padx=10)

    def show_delete_record(self):
        # I-initialize ang frame kung wala pa
        if not hasattr(self, 'delete_records_frame'):
            self.create_delete_record_screen()
        
        # I-load ang listahan ng mga estudyante
        self.student_listbox.delete(0, tk.END)
        self.current_students = self._read_json(self.student_db_file)
        
        for s in self.current_students:
            # I-format: "ID | NAME" para madaling makilala
            self.student_listbox.insert(tk.END, f"{s['id']} | {s['name'].upper()}")
            
        # Linisin ang frames at ipakita ang delete screen
        self.dashboard_frame.pack_forget()
        self.add_student_frame.pack_forget()
        self.grades_frame.pack_forget()
        self.view_records_frame.pack_forget()
        self.update_records_frame.pack_forget()
        self.delete_records_frame.pack(fill="both", expand=True)

    def delete_selected_student(self):
        selected_index = self.student_listbox.curselection()
        
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a student first!")
            return

        # Kunin ang ID mula sa piniling string
        selected_text = self.student_listbox.get(selected_index)
        student_id = selected_text.split(" | ")[0]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student {student_id}?")
        
        if confirm:
            # 1. Alisin sa students.json
            students = self._read_json(self.student_db_file)
            new_students = [s for s in students if s['id'] != student_id]
            self._write_json(self.student_db_file, new_students)

            # 2. Alisin sa grades.json
            grades_list = self._read_json(self.grade_db_file)
            new_grades = [g for g in grades_list if g['id'] != student_id]
            self._write_json(self.grade_db_file, new_grades)

            messagebox.showinfo("Success", "Student record deleted successfully!")
            self.show_delete_record() # I-refresh ang listahan

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRecordSystem(root)
    root.mainloop()
