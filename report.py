import streamlit as st
import pandas as pd
import plotly.express as px
from backend import Expensetracker
import  sqlite3 as sq

exp = Expensetracker()

def app():
    c1, c2, c3 = st.columns([1, 8, 1])
    with c2:
        name = st.text_input("Enter your name to view report", key="report_username")

        if name:
            conn = sq.connect("data.db")
            df_expense = pd.read_sql_query(
                """
                SELECT 
                    date AS Date, 
                    strftime('%m-%Y', date) AS Month, 
                    category AS Category, 
                    'Expense' AS Type, 
                    expense AS Amount, 
                    description AS Description 
                FROM EXPENSE 
                WHERE name = ?
                """,
                conn, params=(name,)
            )

            # Income Data
            df_income = pd.read_sql_query(
                """
                SELECT 
                    date AS Date, 
                    strftime('%m-%Y', date) AS Month, 
                    'Income' AS Category, 
                    'Income' AS Type, 
                    income AS Amount, 
                    description AS Description 
                FROM income 
                WHERE name = ?
                """,
                conn, params=(name,)
            )
            df = pd.concat([df_expense, df_income])
            df["Amount"] = df["Amount"].astype(float)
            with st.sidebar:
                st.markdown("## 🎯 Filters")
                month_filter = st.multiselect("Select Month", options=df["Month"].unique(), default=df["Month"].unique())
                category_filter = st.multiselect("Select Category", options=df["Category"].unique(), default=df["Category"].unique())
                type_filter = st.multiselect("Select Type", options=df["Type"].unique(), default=df["Type"].unique())
            df_filtered = df[
                (df["Month"].isin(month_filter)) &
                (df["Category"].isin(category_filter)) &
                (df["Type"].isin(type_filter))
            ]
            st.markdown("## 📃 Report")
            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            st.markdown("## 📊 Charts")
            col1, col2 = st.columns(2)

            with col1:
                df_exp = df_filtered[df_filtered['Category'] != 'Income']
                if not df_exp.empty:
                    fig_exp = px.bar(df_exp.groupby("Type").sum(numeric_only=True).reset_index(), x="Type", y="Amount", title="Expenses by Type")
                    st.plotly_chart(fig_exp, use_container_width=True)
                else:
                    st.info("No expense data for selected filters.")

            with col2:
                df_inc = df_filtered[df_filtered['Category'] == 'Income']
                if not df_inc.empty:
                    fig_inc = px.bar(df_inc.groupby("Type").sum(numeric_only=True).reset_index(), x="Type", y="Amount", title="Income by Type")
                    st.plotly_chart(fig_inc, use_container_width=True)
                else:
                    st.info("No income data for selected filters.")
            st.markdown("## 💰 Totals")
            total_income = df_inc["Amount"].sum()
            total_expense = df_exp["Amount"].sum()
            savings = total_income - total_expense

            col4, col5, col6 = st.columns(3)
            with col4:
                st.success(f"Total Income : ₹{total_income}")
            with col5:
                st.error(f"Total Expenses : ₹{total_expense}")
            with col6:
                if savings < 0:
                    st.error(f"Total Balance : ₹{savings}")
                elif savings == 0:
                    st.warning(f"Total Balance : ₹{savings}")
                else:
                    st.success(f"Total Balance : ₹{savings}")
            st.markdown("## 🧾 Budget Summary")

            budget_summary = []
            for m in month_filter:
                # Get total expenses for the month
                cur = conn.cursor()
                cur.execute("""
                    SELECT SUM(expense) FROM EXPENSE 
                    WHERE strftime('%m-%Y', date) = ? AND name = ?
                """, (m, name))
                total_exp = cur.fetchone()[0] or 0

                # Get budget for the month
                cur.execute("SELECT amount FROM BUDGET WHERE month = ?", (m,))
                bud = cur.fetchone()
                budget_amount = bud[0] if bud else 0

                # Calculate remaining
                remaining = budget_amount - total_exp

                budget_summary.append({
                    "Month": m,
                    "Budget (₹)": budget_amount,
                    "Spent (₹)": total_exp,
                    "Remaining (₹)": remaining
                })

            df_budget = pd.DataFrame(budget_summary)

            def color_remaining(val):
                if val < 0:
                    return 'color: red'
                elif val == 0:
                    return 'color: orange'
                else:
                    return 'color: green'

            st.dataframe(df_budget.style.applymap(color_remaining, subset=["Remaining (₹)"]),
                         use_container_width=True, hide_index=True)



