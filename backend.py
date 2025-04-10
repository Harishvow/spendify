import datetime
import sqlite3 as sq

class Expensetracker:
    def __init__(self):
        with sq.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS BUDGET(month TEXT PRIMARY KEY, amount REAL)")
            conn.commit()

    def addexpense(self, name, expense, cat, des):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        with sq.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO EXPENSE(name, date, expense, category, description) VALUES (?, ?, ?, ?, ?)",
                (name, date, expense, cat, des)
            )
            conn.commit()

    def viewexpense(self, name, dates):
        with sq.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM EXPENSE WHERE name = ? AND date = ?", (name, dates))
            outs = cursor.fetchone()
            print(outs if outs else "No records found")

    def income(self, name, income, des):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        with sq.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO income(name, date, income, description) VALUES (?, ?, ?, ?)",
                (name, date, income, des)
            )
            conn.commit()

    def resetincome(self):
        with sq.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM income")
            conn.commit()

    def budget_exists(self, month):
        with sq.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM BUDGET WHERE month = ?", (month,))
            return cursor.fetchone() is not None

    def resetexp(self):
        with sq.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM EXPENSE")
            conn.commit()

    def resetbud(self):
        with sq.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM BUDGET")
            conn.commit()

    def setbudget(self, month, amount):
        try:
            with sq.connect("data.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO BUDGET (month, amount) VALUES (?, ?)", (month, amount))
                conn.commit()
        except sq.IntegrityError:
            print("Budget already exists for this month.")
        except sq.Error as e:
            print("Database error while setting budget:", e)

    def getbudget(self, month):
        with sq.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT amount FROM BUDGET WHERE month=?", (month,))
            budget = cursor.fetchone()
            cursor.execute("SELECT SUM(expense) FROM EXPENSE WHERE strftime('%Y-%m', date) = ?", (month,))
            expense = cursor.fetchone()
            budget_amount = budget[0] if budget else 0
            expense_total = expense[0] if expense[0] else 0
            if expense_total > budget_amount:
                print("You reached your limit")
            else:
                print("You are within budget")

    def select(self):
        while True:
            print("1. Add expense")
            print("2. View the expense")
            choice = input("Enter your choice: ")
            if choice == "1":
                name = input("Enter your name: ")
                expense = input("Enter your expense: ")
                cat = input("Enter your category: ")
                des = input("Enter your description: ")
                self.addexpense(name, expense, cat, des)
            else:
                name = input("Enter your name: ")
                dates = input("Enter your date: ")
                self.viewexpense(name, dates)


