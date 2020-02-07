import glob
from time import strftime
import pandas as pd
import time
from time import time
from functools import wraps

def timeit(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        resp = f(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} executed in {end - start:.4f} seconds')
        return (resp, end-start)
    return wrapper

def our_decorator(func):
    def function_wrapper(x):
        print("Before calling " + func.__name__)
        func(x)
        print("After calling " + func.__name__)
    return function_wrapper


def folder_csv_merge(file_prefix, folder_path='', memory='no'):
    """
    file_prefix: if you want to add a prefix to the name of final merged file
    folder_path: no need to declare it. string copied from file explorer to the folder where the files are
    """
    if folder_path == '':
        folder_path = input('Please enter the path where the CSV files are:\n')
    folder_path = folder_path.replace("\\", "/")
    if folder_path[:-1] != "/":
        folder_path = folder_path + "/"

    file_list = glob.glob(folder_path + '*.csv')

    combined = pd.concat([pd.read_csv(f) for f in file_list])
    if memory == 'no':
        combined.to_csv(folder_path + 'combined_{}_{}.csv'.format(file_prefix,
                                                                  strftime("%Y%m%d-%H%M%S")), index=False)
    else:
        return combined
    print('done')


def missing_values_table(df):
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    mis_val_table_ren_columns = mis_val_table.rename(
        columns={0: 'Missing Values', 1: '% of Total Values'})
    mis_val_table_ren_columns = mis_val_table_ren_columns[
        mis_val_table_ren_columns.iloc[:, 1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
    print("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
          "There are " + str(mis_val_table_ren_columns.shape[0]) +
          " columns that have missing values.")
    return mis_val_table_ren_columns


def data_frames(df):
    for dateR, frame in df_grouped_hgs:
        print(f"First 2 entries for {dateR!r}")
        print("------------------------")
        print(frame.head(2), end="\n\n")
