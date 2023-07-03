import pandas as pd
from typing import Dict
from flask import Flask, request
from datetime import datetime, timedelta


app = Flask(__name__)


def load_shifts() -> pd.DataFrame:
    data_path = r'C:\Users\GoMaN\Desktop\GoMaN\Projects\Shifts_service\shifts_data\2023.xlsx'
    features_mapping = {'תאריך': 'date', 'מבצע סופי': 'name'}

    xls = pd.ExcelFile(data_path)
    nagad_df = pd.read_excel(xls, 'נגד תורן')
    officer_df = pd.read_excel(xls, 'קצין תורן')

    nagad_df = preprocess_df(nagad_df, features_mapping)
    officer_df = preprocess_df(officer_df, features_mapping)

    df = pd.concat([nagad_df, officer_df], ignore_index=True)
    df = df.sort_values(by='date')

    return df


def preprocess_df(df: pd.DataFrame, relevant_columns: Dict[str, str]) -> pd.DataFrame:
    temp_df = df.copy()
    temp_df.columns = temp_df.iloc[1]
    temp_df = temp_df[3:]
    temp_df = temp_df[(temp_df.count(axis=1) > 1) == True]
    temp_df = temp_df.loc[:, relevant_columns.keys()]
    temp_df.columns = relevant_columns.values()
    temp_df['date'] = temp_df['date'].apply(lambda x: str(x) + '.2023')
    temp_df['date'] = pd.to_datetime(temp_df['date'], format='mixed', errors='coerce')
    temp_df = temp_df[~temp_df['date'].isnull()]

    return temp_df


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/get_shifts', methods=['GET'])
def get_shifts():
    args = request.args
    date_str = args['date']
    ref_date = datetime.strptime(date_str, '%d.%m.%Y')

    df = load_shifts()
    max_delta = timedelta(days=7)
    min_delta = timedelta(days=0)

    records_in_interval = (min_delta < df['date'] - ref_date) & (df['date'] - ref_date < max_delta)
    filtered_df = df[records_in_interval]

    results = format_results(filtered_df)

    return results


def format_results(filtered_df: pd.DataFrame):
    results = {'open_dates': [{'name': row['name'], 'date': row['date']} for i, row in filtered_df.iterrows()]}
    return results


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
