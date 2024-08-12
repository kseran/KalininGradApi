from sqlalchemy import Table, Column, Integer, String
from database import ContDateBase

users = Table(
    "users",
    ContDateBase.get_metadata(),
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String, unique=True, index=True),
    Column("hashed_password", String),
)
