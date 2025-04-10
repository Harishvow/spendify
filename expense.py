import streamlit as sd
from backend import Expensetracker

exp = Expensetracker()

def app():
    c1, c2 ,c3= sd.columns([1,8,1])

    with c2:
        name = sd.text_input("Enter your name", key="name_input_expense")
        category = sd.selectbox("Select the category",
            ["Food", "Transport", "Entertainment", "Fuel", "Personal", "Electronics", "Others"],
            key="category_input_expense")
        amount = sd.number_input("Enter amount", key="amount_input_expense",min_value=0,
                                 max_value=10000000000,
                                 value=None)
        des = sd.text_input("Enter a description", key="desc_input_expense")
        p1,p2,p3=sd.columns([5,3,2])
        with p1:
            if sd.button("Add Expense", key="add_expense_button"):
                exp.addexpense(name, str(amount), category, des)
                sd.success("Expense added successfully!")
        with p3:
                if sd.button("reset",key="reset_button"):
                   exp.resetexp()

