import pyodbc


server = "DESKTOP-IACHN54\SQLEXPRESS"
database = "CRUD"
username = "sa"
password = "1234"
hex_sec_key = "d5fb8c4fa8bd46638dadc4e751e0d68d"

# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
cnxn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-IACHN54\SQLEXPRESS;DATABASE=CRUD;ENCRYPT=yes;TrustServerCertificate=yes;UID=sa;PWD=1234;"
)
cursor = cnxn.cursor()
