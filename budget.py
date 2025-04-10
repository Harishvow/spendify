import streamlit as sd
import datetime

from click import option
from streamlit import button

import backend
from backend import Expensetracker

exp=Expensetracker()


def app():
    sd.title("📅 Set Monthly Budget")

    c1, c2, c3 = sd.columns(3)

    with c1:
        amount = sd.slider("Select Budget Amount", min_value=1, max_value=100000)


    with c2:
        today = datetime.datetime.now()
        jan1 = datetime.date(today.year, 1, 1)
        dec31 = datetime.date(today.year, 12, 31)

        selected_date = sd.date_input("Select a date in the month you want to budget for", today, min_value=jan1,
                                      max_value=dec31, format="YYYY.MM.DD")
        month_str = selected_date.strftime("%Y-%m")
    with c1:
        if sd.button("Set Budget", key=f"budget-{month_str}-{amount}"):
            if exp.budget_exists(month_str):
                sd.warning(f"⚠️ You already set a budget for {selected_date.strftime('%B %Y')}")
            else:
                exp.setbudget(month_str, amount)
                sd.write(f"✅ Budget of ₹{amount} for {selected_date.strftime('%B %Y')} has been saved!")
    with c2:
        if sd.button("reset",key="reset button"):
            sd.success("your budget has reset successfully")
            exp.resetbud()









