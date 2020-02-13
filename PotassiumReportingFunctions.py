import pandas as pd
import WebsterMiscFunctions

def process_input(hgs_file,qe_file):
    # Import files
    df_qe = pd.read_csv(qe_file, na_values=['.'], sep=";", engine='python')
    df_hgs = pd.read_csv(hgs_file, na_values=['.'], sep=";", engine='python')

    # Clean up data
    df_hgs['NewK'] = pd.to_numeric(df_hgs.K, errors='coerce')
    df_qe['NewK'] = pd.to_numeric(df_qe.K, errors='coerce')

    df_hgs.DTR = pd.to_datetime(df_hgs.DTR, errors='coerce')
    df_qe.DTR = pd.to_datetime(df_qe.DTR, errors='coerce')

    df_hgs.DTC = pd.to_datetime(df_hgs.DTC, errors='coerce')
    df_qe.DTC = pd.to_datetime(df_qe.DTC, errors='coerce')

    df_hgs.FDRPORT = pd.to_datetime(df_hgs.FDRPORT, errors='coerce')
    df_qe.FDRPORT = pd.to_datetime(df_qe.FDRPORT, errors='coerce')

    df_hgs.FDR = pd.to_datetime(df_hgs.FDR, errors='coerce')
    df_qe.FDR = pd.to_datetime(df_qe.FDR, errors='coerce')

    df_hgs.FDAUTH = pd.to_datetime(df_hgs.FDAUTH, errors='coerce')
    df_qe.FDAUTH = pd.to_datetime(df_qe.FDAUTH, errors='coerce')

    df_qe['TravelTime'] = (df_qe.DTR-df_qe.DTC).astype('timedelta64[h]')
    df_hgs['TravelTime'] = (df_hgs.DTR-df_hgs.DTC).astype('timedelta64[h]')

    df_qe['TravelTime'] = (df_qe.DTR-df_qe.DTC).astype('timedelta64[h]')
    df_hgs['TravelTime'] = (df_hgs.DTR-df_hgs.DTC).astype('timedelta64[h]')

    df_hgs.groupby(["FDR", "LOC"])['K'].count()

    return df_hgs, df_qe
