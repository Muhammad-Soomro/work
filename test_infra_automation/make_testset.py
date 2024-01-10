import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv('/home/muhammadasadsoomro/Downloads/TT_cf_ulc_analysis/data_set_tt_30102.csv')
    df['id'].to_csv('/home/muhammadasadsoomro/Desktop/Work/test_infra_automation/ids.txt', index=False, header=False)