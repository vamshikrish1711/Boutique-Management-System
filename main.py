import sys
import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Create a main window
root = tk.Tk()
root.title("SDESIGNERS")

# Database connection setup
mycon = mysql.connector.connect(
    host="localhost", user="Dharani", password="22eg112c12", database="sboutique"
)
mycur = mycon.cursor()

# Function to handle navigation back to the previous window
def navigate_back(window):
    window.withdraw()  # Hide the current window
    if page_stack:
        prev_page = page_stack.pop()
        prev_page.deiconify()  # Show the previous window

# Function to exit the application
def exit_app():
    sys.exit()


# Stack to manage windows for navigation
page_stack = []

# Functions related to Customer Page
def open_customer_window():
    customer_window = tk.Toplevel(root)
    customer_window.title("Customer Page")
    page_stack.append(customer_window)

    create_account_btn = tk.Button(customer_window, text="Create Account", command=create_account)
    create_account_btn.pack()

    sign_in_btn = tk.Button(customer_window, text="Sign In", command=sign_in)
    sign_in_btn.pack()

    back_btn = tk.Button(customer_window, text="Back", command=customer_window.destroy)
    back_btn.pack()

    pass

    



def create_account():
    create_account_window = tk.Toplevel(root)
    create_account_window.title("Create Account")

    import mysql.connector

    mycon = mysql.connector.connect(
        host="localhost", user="Dharani", password="22eg112c12", database="sboutique"
    )

    mycur = mycon.cursor()

    def space():
        for _ in range(1):
            print()

    def check():
        qry = "SELECT cust_id FROM customer;"
        mycur.execute(qry)
        d = mycur.fetchall()
        return [ids[0] for ids in d]

    def cust_ac():
        ask = int(custid_entry.get())  # Fetch customer ID from Entry widget
        list_of_ids = check()  # Obtain existing customer IDs

        if ask in list_of_ids:
            # Customer ID already exists
            messagebox.showinfo(
                "Error", "This Customer ID already exists. Try creating a new one."
            )
        else:
            # Customer ID is unique; proceed with creating the account
            c_det = (
                ask,
                cnam_entry.get(),
                clnam_entry.get(),
                cphno_entry.get(),
                cadrs_entry.get(),
            )

            qry = "insert into customer values(%s,%s,%s,%s,%s,NULL);"
            val = c_det

            mycur.execute(qry, val)
            mycon.commit()
            messagebox.showinfo("Success", "Customer details entered successfully.")

    custid_label = tk.Label(create_account_window, text="Customer ID:")
    custid_label.pack()
    custid_entry = tk.Entry(create_account_window)
    custid_entry.pack()

    cnam_label = tk.Label(create_account_window, text="First Name:")
    cnam_label.pack()
    cnam_entry = tk.Entry(create_account_window)
    cnam_entry.pack()

    clnam_label = tk.Label(create_account_window, text="Last Name:")
    clnam_label.pack()
    clnam_entry = tk.Entry(create_account_window)
    clnam_entry.pack()

    cphno_label = tk.Label(create_account_window, text="Phone Number:")
    cphno_label.pack()
    cphno_entry = tk.Entry(create_account_window)
    cphno_entry.pack()

    cadrs_label = tk.Label(create_account_window, text="Address:")
    cadrs_label.pack()
    cadrs_entry = tk.Entry(create_account_window)
    cadrs_entry.pack()

    submit_btn = tk.Button(create_account_window, text="Submit", command=cust_ac)
    submit_btn.pack()

    back_btn = tk.Button(
        create_account_window, text="Back", command=create_account_window.destroy
    )
    back_btn.pack()


def check():
    mycon = mysql.connector.connect(
        host="localhost", user="Dharani", password="22eg112c12", database="sboutique"
    )
    mycur = mycon.cursor()

    qry = "SELECT cust_id FROM customer;"
    mycur.execute(qry)
    d = mycur.fetchall()

    return [ids[0] for ids in d]


def view_bookings(cust_id):
    def go_back():
        choices_window.deiconify()
        bookings_window.destroy()

    bookings_window = tk.Toplevel(root)
    bookings_window.title("Bookings")

    s = get_bkd_pro(cust_id)
    if s is None or s.strip() == "":
        messagebox.showinfo("Bookings", "You have not booked products yet")
    else:
        d = s.split("_")
        booked_products = "\n".join(d)
        bookings_label = tk.Label(
            bookings_window, text=f"Booked products:\n{booked_products}"
        )
        bookings_label.pack()

    back_btn = tk.Button(bookings_window, text="Back", command=go_back)
    back_btn.pack()  # Places the back button according to the default packing rules


def book_product_window(ask):
    def book():
        pro_id = product_entry.get()  # Get the product ID from the Entry widget

        qry = "SELECT pro_id FROM products;"
        mycur.execute(qry)
        pro_list = mycur.fetchall()
        list_of_products = [i[0] for i in pro_list]

        if pro_id in list_of_products:
            qry = "SELECT bkd_pro FROM customer WHERE cust_id=%s;"
            mycur.execute(qry, (ask,))
            pr = mycur.fetchone()
            if prl := pr[0] or "":
                prl1 = prl + pro_id
                val = f"{prl1}_", ask
            else:
                val = f"{pro_id}_", ask
            _update_customer(
                "UPDATE customer SET bkd_pro=%s WHERE cust_id=%s;",
                val,
                "Your Product is booked!",
            )
            messagebox.showinfo("Success", "Your product is booked!")
        else:
            messagebox.showinfo(
                "Error",
                "This product does not exist. Please enter the correct product ID!",
            )

        book_window.destroy()  # Close the book window after booking

    # Create a new window for booking a product
    book_window = tk.Toplevel(root)
    book_window.title("Book a Product")

    product_label = tk.Label(book_window, text="Enter Product ID:")
    product_label.pack()
    product_entry = tk.Entry(book_window)
    product_entry.pack()

    submit_btn = tk.Button(book_window, text="Submit", command=book)
    submit_btn.pack()

    back_btn = tk.Button(book_window, text="Back", command=book_window.destroy)
    back_btn.pack()
    

def update_self_details(ask, choices_window):
    def update_and_close():
        # Fetch updated values from entry widgets
        updated_values = [entry.get() for entry in entry_list]

        # Update customer details in the database
        qry = "UPDATE customer SET c_nam=%s, c_lnam=%s, c_phno=%s, c_adrs=%s WHERE cust_id=%s;"
        val = tuple(updated_values) + (ask,)
        mycur.execute(qry, val)
        mycon.commit()

        # Show success message
        messagebox.showinfo("Success", "Your details are updated")
        update_window.destroy()
        
    def go_back():
        update_window.destroy()

    update_window = tk.Toplevel(choices_window)
    update_window.title("Update Details")

    qry = (
        "SELECT cust_id, c_nam, c_lnam, c_phno, c_adrs FROM customer WHERE cust_id = %s"
    )
    mycur.execute(qry, (ask,))
    clist = mycur.fetchone()
    flds = ["Name", "Last Name", "Ph.No", "Address"]
    dic = {}
    print("Your existing record is:")

    entry_list = []

    for i in range(4):
        dic[flds[i]] = clist[i + 1]
        label = tk.Label(update_window, text=f"Enter {flds[i]}:")
        label.pack()
        entry = tk.Entry(update_window)
        entry.pack()
        entry.insert(tk.END, clist[i + 1])
        entry_list.append(entry)

    submit_btn = tk.Button(update_window, text="Submit", command=update_and_close)
    submit_btn.pack()

    back_btn = tk.Button(update_window, text="Back", command=go_back)
    back_btn.pack()


def cancel_booked_products(ask):
    def cancel():
        bkd_pro = get_bkd_pro(ask)
        if bkd_pro is None or bkd_pro.strip() == "":
            messagebox.showinfo("Bookings", "You have no bookings to cancel")
        else:
            cw = input(
                "To cancel all products; enter A \nOR enter the product code to cancel: "
            )
            if cw in "Aa":
                qry = "UPDATE customer SET bkd_pro=NULL WHERE cust_id=%s"
                mycur.execute(qry, (ask,))
                mycon.commit()
                messagebox.showinfo("Bookings", "All bookings deleted")
            elif cw in bkd_pro:
                x = bkd_pro[:-1].split("_")
                x.remove(cw)
                updt_pro = ""
                for item in x:
                    updt_pro = updt_pro + item + "_"
                qry = "UPDATE customer SET bkd_pro=%s WHERE cust_id=%s"
                val = (updt_pro, ask)
                _update_customer(qry, val, "Booking Cancelled!")

    def go_back():
        cancel_window.destroy()  # Close the cancel window after the process

    # Create a new window for canceling booked products
    cancel_window = tk.Toplevel(root)
    cancel_window.title("Cancel Booked Products")

    cancel_btn = tk.Button(cancel_window, text="Cancel Bookings", command=cancel)
    cancel_btn.pack()

    if get_bkd_pro(ask) is None or get_bkd_pro(ask).strip() == "":
        not_available_label = tk.Label(cancel_window, text="Not available")
        not_available_label.pack()

    back_btn = tk.Button(cancel_window, text="Back", command=go_back)
    back_btn.pack()
    

def _update_customer(qry, val, success_msg):
    mycur.execute(qry, val)
    mycon.commit()
    print(success_msg)
    pass

def view_available_products():
    products_window = tk.Toplevel(root)
    products_window.title("Available Products")

    qry = "SELECT * FROM products;"
    mycur.execute(qry)
    products = mycur.fetchall()

    if not products:
        messagebox.showinfo("Products", "No products available at the moment.")
    else:
        product_info = "Available Products:\n"
        for product in products:
            product_id, product_name, price, stock = product
            product_info += f"Product ID: {product_id}, Name: {product_name}, Price: {price}, Stock: {stock}\n"

        products_label = tk.Label(products_window, text=product_info)
        products_label.pack()

    back_btn = tk.Button(products_window, text="Back", command=products_window.destroy)
    back_btn.pack()
    pass

def submit_sign_in(custid_entry):
    ask = int(custid_entry.get())
    list_of_ids = check()

    if ask in list_of_ids:
        choices_window = tk.Toplevel(root)
        choices_window.title("Choices")

        def handle_choice():
            ccc = choice_var.get()
            if ccc == "1":
                view_bookings(ask)
            elif ccc == "2":
                book_product_window(ask)  # Open the book product window
            elif ccc == "3":
                update_self_details(ask, choices_window)
            elif ccc == "4":
                cancel_booked_products(ask)
            elif ccc == "5":
                view_available_products()
            elif ccc.lower() == "back":
                messagebox.showinfo("Info", "Successfully logged out")
                choices_window.destroy()
            else:
                messagebox.showinfo(
                    "Info", "Invalid choice. Please enter a valid option."
                )

        choice_var = tk.StringVar()
        choice_var.set("1")  # Default value

        choices_label = tk.Label(choices_window, text="Choose an option:")
        choices_label.pack()

        choices = [
            ("View Bookings", "1"),
            ("Book a Product", "2"),
            ("Update Self Details", "3"),
            ("Cancel Booked Products", "4"),
            ("View Available Products", "5"),
            ("Back", "back"),
        ]

        for text, val in choices:
            radio_btn = tk.Radiobutton(
                choices_window, text=text, variable=choice_var, value=val
            )
            radio_btn.pack()

        submit_choice_btn = tk.Button(
            choices_window, text="Submit", command=handle_choice
        )
        submit_choice_btn.pack()


def sign_in():

    signin_window = tk.Toplevel(root)
    signin_window.title("Sign In")

    signin_custid_label = tk.Label(signin_window, text="Customer ID:")
    signin_custid_label.pack()
    signin_custid_entry = tk.Entry(signin_window)
    signin_custid_entry.pack()

    submit_signin_btn = tk.Button(
        signin_window,
        text="Submit",
        command=lambda: submit_sign_in(signin_custid_entry),
    )
    submit_signin_btn.pack()

    back_btn = tk.Button(signin_window, text="Back", command=signin_window.destroy)
    back_btn.pack()

def view_all_data(table_name):
    qry = f"SELECT * FROM {table_name};"
    mycur.execute(qry)
    data = mycur.fetchall()

    # Display the fetched data
    for row in data:
        print(row)
pass
def view_delivered_records():
    def go_back():
        delivered_records_window.destroy()

    delivered_records_window = tk.Toplevel(root)
    delivered_records_window.title("Delivered Records")

    # Assuming your SQL query retrieves delivered records from a table
    qry = "SELECT * FROM delivered_records;"
    mycur.execute(qry)
    delivered_records = mycur.fetchall()

    if not delivered_records:
        messagebox.showinfo("Delivered Records", "No records available.")
    else:
        record_info = "Delivered Records:\n"
        for record in delivered_records:
            # Modify this based on your record structure
            record_info += f"Record ID: {record[0]}, Product ID: {record[1]}, Quantity: {record[2]}, Date: {record[3]}\n"

        records_label = tk.Label(delivered_records_window, text=record_info)
        records_label.pack()

    back_btn = tk.Button(delivered_records_window, text="Back", command=go_back)
    back_btn.pack()
pass

def add_new_product():
    def submit_new_product():
        new_id = new_id_entry.get()
        new_name = new_name_entry.get()
        new_price = new_price_entry.get()
        new_stock = new_stock_entry.get()

        # Check if the product ID already exists
        qry = "SELECT pro_id FROM products WHERE pro_id = %s;"
        mycur.execute(qry, (new_id,))
        existing_id = mycur.fetchone()

        if existing_id:
            messagebox.showinfo(
                "Error", "This product ID already exists. Try with a different ID."
            )
        else:
            # Insert the new product into the database
            qry = "INSERT INTO products (pro_id, pro_name, price, stock) VALUES (%s, %s, %s, %s);"
            val = (new_id, new_name, new_price, new_stock)
            mycur.execute(qry, val)
            mycon.commit()
            messagebox.showinfo("Success", "New product added successfully.")
            add_product_window.destroy()

    add_product_window = tk.Toplevel(root)
    add_product_window.title("Add New Product")

    new_id_label = tk.Label(add_product_window, text="Product ID:")
    new_id_label.pack()
    new_id_entry = tk.Entry(add_product_window)
    new_id_entry.pack()

    new_name_label = tk.Label(add_product_window, text="Product Name:")
    new_name_label.pack()
    new_name_entry = tk.Entry(add_product_window)
    new_name_entry.pack()

    new_price_label = tk.Label(add_product_window, text="Price:")
    new_price_label.pack()
    new_price_entry = tk.Entry(add_product_window)
    new_price_entry.pack()

    new_stock_label = tk.Label(add_product_window, text="Stock:")
    new_stock_label.pack()
    new_stock_entry = tk.Entry(add_product_window)
    new_stock_entry.pack()

    submit_btn = tk.Button(
        add_product_window, text="Submit", command=submit_new_product
    )
    submit_btn.pack()

    back_btn = tk.Button(
        add_product_window, text="Back", command=add_product_window.destroy
    )
    back_btn.pack()
    pass

def generate_reports_function():
    # Assuming you have a MySQL query to fetch data
    qry = "SELECT * FROM your_table;"
    mycur.execute(qry)
    data = mycur.fetchall()
    

    # Example: Creating a DataFrame from fetched data
    columns = ["Column1", "Column2", "Column3"]  # Replace with your actual column names
    df = pd.DataFrame(data, columns=columns)

    # Generating a basic report using Pandas
    report_name = "report.csv"  # Replace with the desired report name
    df.to_csv(report_name, index=False)

    print(f"Report generated: {report_name}")

def delete_product():
    def perform_deletion():
        product_id = product_id_entry.get()  # Fetch product ID from Entry widget

        qry = "SELECT pro_id FROM products;"
        mycur.execute(qry)
        pro_list = mycur.fetchall()
        list_of_products = [i[0] for i in pro_list]

        if product_id in list_of_products:
            qry = "DELETE FROM products WHERE pro_id=%s;"
            val = (product_id,)
            mycur.execute(qry, val)
            mycon.commit()
            messagebox.showinfo("Success", "Product deleted successfully!")
        else:
            messagebox.showinfo(
                "Error", "Product ID does not exist. Please enter a valid product ID!"
            )

        delete_window.destroy()  # Close the delete window after deletion

    # Create a new window for deleting a product
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Product")

    product_id_label = tk.Label(delete_window, text="Enter Product ID:")
    product_id_label.pack()
    product_id_entry = tk.Entry(delete_window)
    product_id_entry.pack()

    submit_btn = tk.Button(delete_window, text="Delete", command=perform_deletion)
    submit_btn.pack()

    back_btn = tk.Button(delete_window, text="Back", command=delete_window.destroy)
    back_btn.pack()
pass

def open_employee_window():
    employee_window = tk.Toplevel(root)
    def navigate_back():
        employee_window.withdraw()  # Hide the current employee window
        if page_stack:
            prev_page = page_stack.pop()  # Get the previous page from the stack
            prev_page.deiconify()  # Show the previous page

    employee_window = tk.Toplevel(root)
    employee_window.title("Employee Page")
    page_stack.append(employee_window)

    view_delivered_records_btn = tk.Button(
        employee_window, text="View Delivered Records", command=view_delivered_records
    )
    view_delivered_records_btn.pack()

    add_new_product_btn = tk.Button(
        employee_window, text="Add New Product", command=add_new_product
    )
    add_new_product_btn.pack()
    
    view_customer_data_btn = tk.Button(
        employee_window, text="View Customer Data", command=lambda: view_all_data("customer")
    )
    view_customer_data_btn.pack()

    delete_product_btn = tk.Button(
        employee_window, text="Delete Product", command=delete_product
    )
    delete_product_btn.pack()

    back_btn = tk.Button(employee_window, text="Back", command=navigate_back)
    back_btn.pack()
    
def view_all_data(table_name):
    view_data_window = tk.Toplevel(root)
    view_data_window.title(f"View {table_name.capitalize()} Data")

    qry = f"SELECT * FROM {table_name};"
    mycur.execute(qry)
    data = mycur.fetchall()

    if not data:
        messagebox.showinfo("No Data", f"No data available in {table_name} table.")
    else:
        for row in data:
            # Display the fetched data in a suitable format within the window
            # Modify this based on your preferences
            data_label = tk.Label(view_data_window, text=row)
            data_label.pack()

    back_btn = tk.Button(view_data_window, text="Back", command=view_data_window.destroy)
    back_btn.pack()
pass
def generate_reports_function():
    def generate_sales_report():
        # Code to generate a sales report
        pass

    def generate_inventory_report():
        # Code to generate an inventory report
        pass

    reports_window = tk.Toplevel(root)
    reports_window.title("Generate Reports")

    sales_report_btn = tk.Button(
        reports_window, text="Generate Sales Report", command=generate_sales_report
    )
    sales_report_btn.pack()

    inventory_report_btn = tk.Button(
        reports_window, text="Generate Inventory Report", command=generate_inventory_report
    )
    inventory_report_btn.pack()


def manage_employees_function():
    def add_employee():
        # Code to add a new employee to the database
        pass

    def delete_employee():
        # Code to delete an employee from the database
        pass

    def update_employee():
        # Code to update employee details in the database
        pass

    manage_employees_window = tk.Toplevel(root)
    manage_employees_window.title("Manage Employees")

    add_employee_btn = tk.Button(
        manage_employees_window, text="Add Employee", command=add_employee
    )
    add_employee_btn.pack()

    delete_employee_btn = tk.Button(
        manage_employees_window, text="Delete Employee", command=delete_employee
    )
    delete_employee_btn.pack()

    update_employee_btn = tk.Button(
        manage_employees_window, text="Update Employee", command=update_employee
    )
    update_employee_btn.pack()
pass
def open_admin_window():
    def go_back():
        admin_window.withdraw()
        if page_stack:
            prev_page = page_stack.pop()
            prev_page.deiconify()

    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Page")
    page_stack.append(admin_window)

    # ... (existing buttons/functionality)

    
    # Rest of your admin page code...

    # Add buttons and functionality for admin actions
    view_delivered_records_btn = tk.Button(
        admin_window, text="View Delivered Records", command=view_delivered_records
    )
    view_delivered_records_btn.pack()

    add_new_product_btn = tk.Button(
        admin_window, text="Add New Product", command=add_new_product
    )
    add_new_product_btn.pack()

    delete_product_btn = tk.Button(
        admin_window, text="Delete Product", command=delete_product
    )
    delete_product_btn.pack()

    generate_reports_btn = tk.Button(
        admin_window, text="Generate Reports", command=generate_reports_function
    )
    generate_reports_btn.pack()

    manage_employees_btn = tk.Button(
        admin_window, text="Manage Employees", command=manage_employees_function
    )
    manage_employees_btn.pack()

    back_btn = tk.Button(admin_window, text="Back", command=go_back)
    back_btn.pack()
    pass



img = tk.PhotoImage(file="/Users/vamshi/Music/Music/1_row_2.gif")
img_label = tk.Label(root, image=img)
img_label.pack()


button_actions = {
    "Customer": open_customer_window,
    "Employee": open_employee_window,
    "Admin": open_admin_window,
    "Exit": exit_app,
    # Add more button actions as needed
}

# Button creation loop
for button_action, action_function in button_actions.items():
    btn = tk.Button(root, text=button_action, command=action_function)
    btn.pack()
# Stack to manage windows for navigation
def handle_button_click(action):
    action_function = button_actions.get(action)
    if action_function:
        action_function()



root.mainloop()
