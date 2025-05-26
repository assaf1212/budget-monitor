
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CashflowEntry(Base):
    __tablename__ = 'cashflow'

    id = Column(Integer, primary_key=True)
    month = Column(String)
    salary1 = Column(Float)
    salary2 = Column(Float)
    credit_expense = Column(Float)
    fixed_expense = Column(Float)
    total_income = Column(Float)
    total_expense = Column(Float)
    net_cashflow = Column(Float)
