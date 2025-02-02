import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Create the database and table if not already exists
def create_db():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    
    # Create the contacts table if it doesn't exist, including the phone number column
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        age INTEGER,
        dob TEXT,
        group_name TEXT,
        nickname TEXT,
        notes TEXT,
        website TEXT,
        organization TEXT,
        phone_number TEXT
    )
    ''')

    # Check if the phone_number column exists, if not, add it
    cursor.execute("PRAGMA table_info(contacts)")
    columns = [column[1] for column in cursor.fetchall()]
    if "phone_number" not in columns:
        cursor.execute("ALTER TABLE contacts ADD COLUMN phone_number TEXT")
    
    conn.commit()
    conn.close()

# Function to insert contact data into the database
def insert_contact():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    age = entry_age.get()
    dob = entry_dob.get()
    group_name = entry_group.get()
    nickname = entry_nickname.get()
    notes = entry_notes.get()
    website = entry_website.get()
    organization = entry_organization.get()
    phone_number = entry_phone_number.get()

    # t first name, last name, and phone number are provided
    if first_name == "" or last_name == "" or phone_number == "":
        messagebox.showerror("Input Error", "First Name, Last Name, and Phone Number are required fields.")
        return

    # Connect to SQLite database and insert contact
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO contacts (first_name, last_name, email, age, dob, group_name, nickname, notes, website, organization, phone_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, email, age, dob, group_name, nickname, notes, website, organization, phone_number))

    conn.commit()
    conn.close()

   
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_dob.delete(0, tk.END)
    entry_group.delete(0, tk.END)
    entry_nickname.delete(0, tk.END)
    entry_notes.delete(0, tk.END)
    entry_website.delete(0, tk.END)
    entry_organization.delete(0, tk.END)
    entry_phone_number.delete(0, tk.END)

   
    load_contacts()

def load_contacts():
    listbox_contacts.delete(0, tk.END)
    
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    
    for contact in contacts:
       
        listbox_contacts.insert(tk.END, f'{contact[0]} - {contact[1]} {contact[2]} - {contact[3]} - {contact[11]}')
    
    conn.close()

def delete_contact():
    try:
       
        selected_contact = listbox_contacts.curselection()[0]
        contact_text = listbox_contacts.get(selected_contact)
        
        
        contact_id = contact_text.split(" - ")[0]
        
       
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
        conn.commit()
        conn.close()

       
        load_contacts()
        messagebox.showinfo("Success", "Contact deleted successfully.")
    
    except IndexError:
        messagebox.showerror("Selection Error", "Please select a contact to delete.")

root = tk.Tk()
root.title("Contact List Application")
root.geometry("800x600")

root.config(bg="#87CEEB")

create_db()

label_first_name = ttk.Label(root, text="First Name", background="#87CEEB")
label_first_name.pack(pady=5)
entry_first_name = ttk.Entry(root, width=40)
entry_first_name.pack(pady=5)

label_last_name = ttk.Label(root, text="Last Name", background="#87CEEB")
label_last_name.pack(pady=5)
entry_last_name = ttk.Entry(root, width=40)
entry_last_name.pack(pady=5)

label_email = ttk.Label(root, text="Email", background="#87CEEB")
label_email.pack(pady=5)
entry_email = ttk.Entry(root, width=40)
entry_email.pack(pady=5)

label_age = ttk.Label(root, text="Age", background="#87CEEB")
label_age.pack(pady=5)
entry_age = ttk.Entry(root, width=40)
entry_age.pack(pady=5)

label_dob = ttk.Label(root, text="Date of Birth", background="#87CEEB")
label_dob.pack(pady=5)
entry_dob = ttk.Entry(root, width=40)
entry_dob.pack(pady=5)

label_group = ttk.Label(root, text="Group", background="#87CEEB")
label_group.pack(pady=5)
entry_group = ttk.Entry(root, width=40)
entry_group.pack(pady=5)

label_nickname = ttk.Label(root, text="Nickname", background="#87CEEB")
label_nickname.pack(pady=5)
entry_nickname = ttk.Entry(root, width=40)
entry_nickname.pack(pady=5)

label_notes = ttk.Label(root, text="Notes", background="#87CEEB")
label_notes.pack(pady=5)
entry_notes = ttk.Entry(root, width=40)
entry_notes.pack(pady=5)

label_website = ttk.Label(root, text="Website", background="#87CEEB")
label_website.pack(pady=5)
entry_website = ttk.Entry(root, width=40)
entry_website.pack(pady=5)

label_organization = ttk.Label(root, text="Organization", background="#87CEEB")
label_organization.pack(pady=5)
entry_organization = ttk.Entry(root, width=40)
entry_organization.pack(pady=5)

label_phone_number = ttk.Label(root, text="Phone Number", background="#87CEEB")
label_phone_number.pack(pady=5)
entry_phone_number = ttk.Entry(root, width=40)
entry_phone_number.pack(pady=5)

# Add button
button_add_contact = ttk.Button(root, text="Add Contact", command=insert_contact)
button_add_contact.pack(pady=20)

# Delete button
button_delete_contact = ttk.Button(root, text="Delete Contact", command=delete_contact)
button_delete_contact.pack(pady=10)

# Listbox to display contacts
listbox_contacts = tk.Listbox(root, height=10, width=50, selectmode=tk.SINGLE)
listbox_contacts.pack(pady=10)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=listbox_contacts.yview)
scrollbar.pack(side="right", fill="y")
listbox_contacts.config(yscrollcommand=scrollbar.set)

load_contacts()

root.mainloop()



