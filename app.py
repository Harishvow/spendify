import streamlit as sd
import sqlite3 as sq
import datetime
from streamlit_option_menu import option_menu
import expense
import income
import budget
import report

sql = sq.connect("data.db")
c = sql.cursor()
c.execute("CREATE TABLE IF NOT EXISTS budget (month TEXT PRIMARY KEY, amount REAL)")
sql.commit()


def run():
    sd.markdown("<h1 style='text-align: center; color: #FF4B4B;'>💸 $pendify</h1>", unsafe_allow_html=True)


    option = option_menu(
        menu_title=None,
        options=["Account", "Expense", "Income", "Set budget", "Report"],
        orientation="horizontal",
        icons=["person-fill", "cash-coin", "cash", "cash-bank", "file-earmark-bar-graph-fill"],
        default_index=0,
    )

    if option == "Expense":
        expense.app()
    elif option =="Income":
        income.app()
    elif option =="Set budget":
        budget.app()
    elif option=="Report":
        report.app()
    elif option == "Account":
        sd.subheader("👤 Account Info")
        sd.info("Account management coming soon...")

run()