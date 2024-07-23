import sqlite3
from flask import Flask,jsonify
import json
import requests
import schedule
import time
from datetime import datetime, timedelta



def loadfundings():
    
        
    query="SELECT * FROM fundings"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,)
        funds = cursor.fetchall()
        
        if funds:
            columns = [column[0] for column in cursor.description]
            funds_list = []
            for fund in funds:
                fund_dict = dict(zip(columns, fund))
                funds_list.append(fund_dict)
            print(funds_list)
            return funds_list
        else:
            return {'message': 'No funds found'}
    except sqlite3.Error as e:
        print('Error:', e)
        return {'message': 'An error occurred while loading funds'}
    finally:
        conn.close()

       
def updateFunding(data):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    for item in data:
        cursor.execute('''
        INSERT INTO fundings (
            public_private,
            type_of_source,
            name_of_source,
            type_of_disbursement_channel,
            name_of_disbursement_channel,
            name_of_funding_opportunity,
            financial_instrument,
            size_of_investment,
            investment_opportunity_info,
            direct_use,
            sectors,
            fund_contact_name,
            fund_contact_email,
            fund_contact_number,
            fund_contact_website
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item["Public/ Private"],
            item["Type of source/ Intermediary of finance"],
            item["Name of  source/ Intermediary of finance"],
            item["Type of disbursement channel "],
            item["Name of  disbursment channel"],
            item["Name of funding opportunity"],
            item["Financial instrument"],
            item["Size of investment"],
            item["Investment opportunity information"],
            item["Direct Use"],
            item["Sector(s)"],
            item["Fund Contact Details / Contact Name"],
            item["Fund Contact E-mail"],
            item["Fund Contact Number"],
            item["Fund Contact Website"]
        ))

    conn.commit()
    conn.close()


def fetch_search_criteria():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

   
    query = "SELECT * FROM fundings"
    cursor.execute(query,)
    rows = cursor.fetchall()

   
    criteria_list = []
    for row in rows:
        criteria = {
            "Type_of_organisation_seeking_funding": row[1],
            "financial_sector_type": row[2],
            "Type_of_Investment_Instrument": row[3],
            "type_of_financing_organisation": row[4],
           # "Type_of_EIP_initiatives_search": row[5],
          #  "Name_financing_organisation": row[6],
          #  "Fund_name": row[7],
          #  "Specific_focus_of_funding": row[8],
          #  "EIP_initiatives_result": row[9],
          #  "Finance_threshhold": row[10],
           # "Eligibility_criteria": row[11],
            "Weblink": row[12],
            "Contact_details": row[13],
            #"Investment_opportunity_information": row[14],
            #"Questionaire_with_financing_institution2": row[15]
        }
        criteria_list.append(criteria)

    conn.close()
    return criteria_list


def search_web(criteria):
    api_key = 'AIzaSyAqRhITpdaLI-osXVA3SvarQADy_ZX_0Xs' 
    search_engine_id = 'a3e8b272ad2b14296'  
    criteria = [value for value in criteria.values() if value is not None]
    query = ' '.join(criteria)

    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}'

    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        scheduled_task()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return None


def update_database(data, criteria):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    if data is not None and 'items' in data:
        for result in data['items']:
            title = result.get('title', '')
            url = result.get('link', '')
            description = result.get('snippet', '')

            print(f"URL: {url}")
            print(f"Updated database for criteria: {criteria['Type_of_organisation_seeking_funding']}")
            print(f"Title: {title}")
            print(f"Description: {description}")
            print("\n")  # Add a separator between entries

        conn.commit()
        conn.close()

def run_task():
    search_criteria_list = fetch_search_criteria()
    for criteria in search_criteria_list:
        search_results = search_web(criteria)
        update_database(search_results, criteria)

def calculate_next_run_date():
    today = datetime.today()
    next_run_date = today + timedelta(days=90)  # Approximation for 3 months
    return next_run_date

next_run_date = calculate_next_run_date()

def scheduled_task():
    global next_run_date
    today = datetime.today().date()
    if today >= next_run_date.date():
        run_task()
        next_run_date = calculate_next_run_date()

