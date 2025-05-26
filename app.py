import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from database import Session as DBSession
from models import CashflowEntry

st.set_page_config(page_title="תזרים עם DB", layout="wide")

# --- סרגל צד ---
st.sidebar.title("📂 תפריט ניווט")
menu_choice = st.sidebar.radio("בחר פעולה:", [
    "📥 הזנת חודש חדש",
    "📤 העלאת CSV",
    "📅 צפייה בנתונים"
])

st.title("📊 תזרים אישי עם מסד נתונים")

if menu_choice == "📥 הזנת חודש חדש":
    with st.form("add_data"):
        st.subheader("📝 הזנת חודש חדש")
        month = st.selectbox("חודש", ["ינואר", "פברואר", "מרץ", "אפריל", "מאי"])
        salary1 = st.number_input("משכורת 1", value=0)
        salary2 = st.number_input("משכורת 2", value=0)
        credit_expense = st.number_input("הוצאות אשראי", value=0)
        submitted = st.form_submit_button("שמור")

    if submitted:
        session = DBSession()
        total_income = salary1 + salary2
        fixed_expense = 12000 + 5400
        total_expense = fixed_expense + credit_expense
        net_cashflow = total_income - total_expense

        entry = CashflowEntry(
            month=month,
            salary1=salary1,
            salary2=salary2,
            credit_expense=credit_expense,
            fixed_expense=fixed_expense,
            total_income=total_income,
            total_expense=total_expense,
            net_cashflow=net_cashflow,
        )
        session.add(entry)
        session.commit()
        session.close()
        st.success("✅ הנתונים נשמרו במסד הנתונים")

elif menu_choice == "📤 העלאת CSV":
    st.subheader("📤 טעינת נתונים מקובץ CSV")
    uploaded_csv = st.file_uploader("בחר קובץ CSV (כמו data.csv)", type=["csv"])
    if uploaded_csv is not None:
        df_csv = pd.read_csv(uploaded_csv)
        st.write("תצוגה מקדימה של הקובץ:")
        st.dataframe(df_csv)

        if st.button("📥 טען את הנתונים למסד הנתונים"):
            session = DBSession()
            for _, row in df_csv.iterrows():
                entry = CashflowEntry(
                    month=row["חודש"],
                    salary1=0,
                    salary2=0,
                    credit_expense=row["אשראי"],
                    fixed_expense=row["הוצאות קבועות"],
                    total_income=row["משכורות"],
                    total_expense=row['סה"כ הוצאות'],
                    net_cashflow=row["תזרים נטו"]
                )
                session.add(entry)
            session.commit()
            session.close()
            st.success("✅ כל הנתונים מהקובץ נטענו למסד הנתונים בהצלחה!")

elif menu_choice == "📅 צפייה בנתונים":
    session = DBSession()
    entries = session.query(CashflowEntry).all()
    if entries:
        st.subheader("📅 טבלת תזרים חודשי")
        data = [{
            "חודש": e.month,
            "משכורות": e.total_income,
            "הוצאות": e.total_expense,
            "תזרים נטו": e.net_cashflow
        } for e in entries]
        st.dataframe(data)
    else:
        st.info("אין נתונים להצגה.")
    session.close()
