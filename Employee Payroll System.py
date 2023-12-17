import time
from tkinter import *
import tkinter.messagebox
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="mydatabase"
)

mycursor = mydb.cursor()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS employee_data (
        NI INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL,
        employer VARCHAR(255) NOT NULL,
        ni_number VARCHAR(255) NOT NULL,
        hours_worked FLOAT NOT NULL,
        wages_hour FLOAT NOT NULL,
        tax FLOAT NOT NULL,
        overtime FLOAT NOT NULL,
        gross_pay FLOAT NOT NULL,
        net_pay FLOAT NOT NULL
    )
''')
mydb.commit()

root = Tk()
root.title("Employee Payroll System")
root.geometry('1350x1050')
root.configure(background="beige")

Tops = Frame(root, width=1350, height=50, bd=8, bg="#00C957")
Tops.pack(side=TOP)

f1 = Frame(root, width=600, height=600, bd=8, bg="#00C957")
f1.pack(side=LEFT)
f2 = Frame(root, width=300, height=700, bd=8, bg="#00C957")
f2.pack(side=RIGHT)

fla = Frame(f1, width=600, height=200, bd=8, bg="lightblue")
fla.pack(side=TOP)
flb = Frame(f1, width=300, height=600, bd=8, bg="lightblue")
flb.pack(side=TOP)

lblinfo = Label(Tops, font=('arial', 45, 'bold'), text="Employee Payment Management system ", bd=10, bg="azure1", fg="green")
lblinfo.grid(row=0, column=0)

def exit_system():
    exit_confirm = tkinter.messagebox.askyesno("Employee System", "Do you want to exit the system?")
    if exit_confirm > 0:
        root.destroy()
        return

def reset_fields():
    Name.set("")
    Address.set("")
    HoursWorked.set("")
    wageshour.set("")
    Payable.set("")
    Taxable.set("")
    NetPayable.set("")
    GrossPayable.set("")
    OverTimeBonus.set("")
    Employer.set("")
    NINumber.set("")
    txtpayslip.delete("1.0", END)

def enter_info():
    txtpayslip.delete("1.0", END)
    txtpayslip.insert(END, "\t\tPay Slip\n\n")
    txtpayslip.insert(END, "Name :\t\t" + Name.get() + "\n\n")
    txtpayslip.insert(END, "Address :\t\t" + Address.get() + "\n\n")
    txtpayslip.insert(END, "Employer :\t\t" + Employer.get() + "\n\n")
    txtpayslip.insert(END, "IN Number :\t\t" + NINumber.get() + "\n\n")
    txtpayslip.insert(END, "Hours Worked :\t\t" + HoursWorked.get() + "\n\n")
    txtpayslip.insert(END, "Net Payable :\t\t" + NetPayable.get() + "\n\n")
    txtpayslip.insert(END, "Wages per hour :\t\t" + wageshour.get() + "\n\n")
    txtpayslip.insert(END, "Tax Paid :\t\t" + Taxable.get() + "\n\n")
    txtpayslip.insert(END, "Payable :\t\t" + Payable.get() + "\n\n")

    try:
        hours_worked = float(HoursWorked.get())
        wages_hour = float(wageshour.get())
        tax = float(Taxable.get())

        overtime = 0.0
        if hours_worked > 40:
            overtime = (hours_worked - 40) * wages_hour * 1.5

        gross_pay = hours_worked * wages_hour + overtime
        net_pay = gross_pay - tax

        mycursor.execute("INSERT INTO employee_data (name, address, employer, ni_number, hours_worked, wages_hour, tax, overtime, gross_pay, net_pay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                          (Name.get(), Address.get(), Employer.get(), NINumber.get(), hours_worked, wages_hour, tax, overtime, gross_pay, net_pay))
        mydb.commit()
        tkinter.messagebox.showinfo("Success", "Data inserted into MySQL successfully")
    except ValueError as ve:
        tkinter.messagebox.showerror("Error", f"ValueError: {ve}\nPlease make sure numeric fields contain valIN Numbers.")
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"Error inserting data into MySQL: {str(e)}")


def calculate_weekly_wages():
    txtpayslip.delete("1.0", END)

    # Check if wageshour and HoursWorked are not empty
    if not wageshour.get() or not HoursWorked.get():
        tkinter.messagebox.showerror("Error", "Please enter both hourly rate and hours worked.")
        return

    try:
        hours_worked_per_week = float(HoursWorked.get())
        wages_per_hour = float(wageshour.get())

        if hours_worked_per_week < 0 or wages_per_hour < 0:
            tkinter.messagebox.showerror("Error", "Please enter non-negative values for hours worked and hourly rate.")
            return

        pay_due = wages_per_hour * hours_worked_per_week
        payment_due =  "{:.2f}".format(pay_due)
        Payable.set(payment_due)

        tax = pay_due * 0.2
        taxable =  "{:.2f}".format(tax)
        Taxable.set(taxable)

        net_pay = pay_due - tax
        net_pays =  "{:.2f}".format(net_pay)
        NetPayable.set(net_pays)

        if hours_worked_per_week > 40:
            overtime_hours = (hours_worked_per_week - 40) + wages_per_hour * 1.5
            overtime = "{:.2f}".format(overtime_hours)
            OverTimeBonus.set(overtime)
        else:
            OverTimeBonus.set("0.00")

    except ValueError as ve:
        tkinter.messagebox.showerror("Error", f"ValueError: {ve}\nPlease make sure numeric fields contain valIN Numbers.")
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"Error in calculating weekly wages: {str(e)}")


# Variables
Name = StringVar()
Address = StringVar()
HoursWorked = StringVar()
wageshour = StringVar()
Payable = StringVar()
Taxable = StringVar()
NetPayable = StringVar()
GrossPayable = StringVar()
OverTimeBonus = StringVar()
Employer = StringVar()
NINumber = StringVar()
DateOfOrder = StringVar()

DateOfOrder.set(time.strftime("%d/%m/%Y"))

# Labels
lblName = Label(fla, text="Name", font=('arial', 16, 'bold'), bd=20, fg="red", bg="lightblue").grid(row=0, column=0)
lblAddress = Label(fla, text="Address", font=('arial', 16, 'bold'), bd=20, fg="red", bg="lightblue").grid(row=0, column=2)
lblEmployer = Label(fla, text="Employer", font=('arial', 16, 'bold'), bd=20, fg="red", bg="lightblue").grid(row=1, column=0)
lblNINumber = Label(fla, text="IN Number", font=('arial', 16, 'bold'), bd=20, fg="red", bg="lightblue").grid(row=1, column=2)
lblHoursWorked = Label(fla, text="Hours Worked", font=('arial', 16, 'bold'), bd=20, fg="red", bg="lightblue").grid(row=2, column=0)
lblHourlyRate = Label(fla, text="Hourly Rate", font=('arial', 16, 'bold'), bd=20, fg="red", bg="lightblue").grid(row=2, column=2)
lblTax = Label(fla, text="Tax", font=('arial', 16, 'bold'), bd=20, anchor='w', fg="red", bg="lightblue").grid(row=3, column=0)
lblOverTime = Label(fla, text="OverTime", font=('arial', 16, 'bold'), bd=20, fg="red", bg="lightblue").grid(row=3, column=2)
lblGrossPay = Label(fla, text="GrossPay", font=('arial', 16, 'bold'), bd=20, fg="red", bg="lightblue").grid(row=4, column=0)
lblNetPay = Label(fla, text="Net Pay", font=('arial', 16, 'bold'), bd=20, fg="red", bg="lightblue").grid(row=4, column=2)

# Entry Widgets
etxname = Entry(fla, textvariable=Name, font=('arial', 16, 'bold'), bd=16, width=22, justify='left')
etxname.grid(row=0, column=1)

etxaddress = Entry(fla, textvariable=Address, font=('arial', 16, 'bold'), bd=16, width=22, justify='left')
etxaddress.grid(row=0, column=3)

etxemployer = Entry(fla, textvariable=Employer, font=('arial', 16, 'bold'), bd=16, width=22, justify='left')
etxemployer.grid(row=1, column=1)

etxhoursworked = Entry(fla, textvariable=HoursWorked, font=('arial', 16, 'bold'), bd=16, width=22, justify='left')
etxhoursworked.grid(row=2, column=1)

etxwagesperhours = Entry(fla, textvariable=wageshour, font=('arial', 16, 'bold'), bd=16, width=22, justify='left')
etxwagesperhours.grid(row=2, column=3)

etxnin = Entry(fla, textvariable=NINumber, font=('arial', 16, 'bold'), bd=16, width=22, justify='left')
etxnin.grid(row=1, column=3)

etxgrosspay = Entry(fla, textvariable=Payable, font=('arial', 16, 'bold'), bd=16, width=22, justify='left')
etxgrosspay.grid(row=4, column=1)

etxnetpay = Entry(fla, textvariable=NetPayable, font=('arial', 16, 'bold'), bd=16, width=22, justify='left')
etxnetpay.grid(row=4, column=3)

etxtax = Entry(fla, textvariable=Taxable, font=('arial', 16, 'bold'), bd=16, width=22, justify='left')
etxtax.grid(row=3, column=1)

etxovertime = Entry(fla, textvariable=OverTimeBonus, font=('arial', 16, 'bold'), bd=16, width=22, justify='left')
etxovertime.grid(row=3, column=3)

# Text Widget
payslip = Label(f2, textvariable=DateOfOrder, font=('arial', 21, 'bold'), fg="red", bg="#00C957").grid(row=0, column=0)
txtpayslip = Text(f2, height=22, width=34, bd=16, font=('arial', 13, 'bold'), fg="green", bg="cyan2")
txtpayslip.grid(row=1, column=0)

# Buttons
btnsalary = Button(flb, text='Weekly Salary', padx=16, pady=16, bd=8, font=('arial', 16, 'bold'), width=14, fg="white", bg="darkgreen", command=calculate_weekly_wages)
btnsalary.grid(row=0, column=0)

btnreset = Button(flb, text='Reset', padx=16, pady=16, bd=8, font=('arial', 16, 'bold'), width=14, command=reset_fields, fg="white", bg="darkgreen")
btnreset.grid(row=0, column=1)

btnpayslip = Button(flb, text='View Payslip', padx=16, pady=16, bd=8, font=('arial', 16, 'bold'), width=14, command=enter_info, fg="white", bg="darkgreen")
btnpayslip.grid(row=0, column=2)

btnexit = Button(flb, text='Exit System', padx=16, pady=16, bd=8, font=('arial', 16, 'bold'), width=14, command=exit_system, fg="white", bg="darkgreen")
btnexit.grid(row=0, column=3)

root.mainloop()
