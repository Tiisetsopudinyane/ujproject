import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('blog.db')

# Create a cursor object
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS fundings (
        id INTEGER PRIMARY KEY,
        public_private TEXT,
        type_of_source TEXT,
        name_of_source TEXT,
        type_of_disbursement_channel TEXT,
        name_of_disbursement_channel TEXT,
        name_of_funding_opportunity TEXT,
        financial_instrument TEXT,
        size_of_investment TEXT,
        investment_opportunity_info TEXT,
        direct_use TEXT,
        sectors TEXT,
        fund_contact_name TEXT,
        fund_contact_email TEXT,
        fund_contact_number TEXT,
        fund_contact_website TEXT
    )
''')

conn.close()