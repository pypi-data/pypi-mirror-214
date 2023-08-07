import mysql.connector
import requests
import hashlib
from . import api
import json
from dataclasses import dataclass

@dataclass()
class DataBase():
    cnx: object #mysql.connector.MySQLConnection
    cur: object #mysql.connector.cursor.CMySQLCursor


def get_credentials(api_key, api_schema, db_schema):
    response = requests.get(f"{api_schema}/api/db_credentials", headers={'key': api_key, 'db':db_schema}).json()
    if response['msg'] == 'success':
        return response['data']
    else:
        print(response)
        return None


def get(api_key, api_schema=None, db_schema=None,  buffered=True, dictionary=False, dc=False):
    if not api_schema:
        api_schema = api.prod

    credentials = get_credentials(api_key=api_key, api_schema=api_schema, db_schema=db_schema)
    if not credentials:
        return None, None
    cnx = mysql.connector.connect(
        user=credentials['user'],
        password=credentials['password'],
        host=credentials['host'],
        database=credentials['database']
    )
    
    cur = cnx.cursor(buffered=buffered, dictionary=dictionary)
    if dc:
        return DataBase(cnx, cur)
    else:
        return cnx, cur


def convert_json(records):
    """
    checks if column title has '_json' in string and converts to dict
    make sure that all json columns have _json in title (and only json columns)
    """
    if records and isinstance(records[0], dict):
        for record in records:
            for column, value in record.items():
                if '_json' in column:
                    record[column] = json.loads(value)
    return records



def null2None(records, dictionary=True):
    result = []
    for record in records:
        if isinstance(record, dict):
            for col_name, val in record.items():
                if val == 'null':
                    record[col_name] = None
        else:
            record = list(record)
            for i, val in enumerate(record):
                if val == 'null':
                    record[i] = None
            record = tuple(record)

        result.append(record)
    return result

if __name__ == '__main__':
    cnx, cur = get(api_key='qV8fHsJymtPKcco@X23k*2GwqNQG.7-2mPya4aLrXeCF.dkKiX')
    print(type(cnx), type(cur))