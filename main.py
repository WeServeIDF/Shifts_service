from typing import List

import pandas as pd


def main():
    data_path = r'C:\Users\GoMaN\Desktop\GoMaN\Projects\Shifts_service\shifts_data\2023.xlsx'
    relevant_columns = ['תאריך', 'מבצע סופי']

    xls = pd.ExcelFile(data_path)
    nagad_df = pd.read_excel(xls, 'נגד תורן')
    officer_df = pd.read_excel(xls, 'קצין תורן')

    nagad_df = preprocess_df(nagad_df, relevant_columns)
    officer_df = preprocess_df(officer_df, relevant_columns)

    print(nagad_df)


def preprocess_df(df: pd.DataFrame, relevant_columns: List[str]) -> pd.DataFrame:
    temp_df = df.copy()
    temp_df.columns = temp_df.iloc[1]
    temp_df = temp_df[3:]
    temp_df = temp_df[(temp_df.count(axis=1) > 1) == True]
    temp_df = temp_df.loc[:, relevant_columns]
    temp_df['תאריך'] = temp_df['תאריך'].apply(lambda x: str(x) + '.2023')

    return temp_df


if __name__ == "__main__":
    main()
