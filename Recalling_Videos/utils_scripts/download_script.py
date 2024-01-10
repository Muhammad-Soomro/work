import boto3
import pandas as pd 
import os
from tqdm import tqdm

s3 = boto3.client('s3')

if __name__ == '__main__':
    df = pd.read_csv('/home/muhammadasadsoomro/Desktop/Motive/Recalling_Videos/utils_scripts/cam_media.csv')
    df.rename(columns={
        'DPE_OFFLINE_ID' : 'OFFLINE_ID',
        "ID" : "CM_ID"
    } , inplace=True)
    error_index = list()
    recalled_status_df = df.copy()
    videos_dl_dir = '/home/muhammadasadsoomro/Desktop/Motive/Lane_Assist/Datasets/Long_Videos'
    for i in tqdm(recalled_status_df.index):
        try:
            vid_filename = f"front_facing-{recalled_status_df.loc[i, 'OFFLINE_ID']}.mp4"
            cm_id = recalled_status_df.loc[i, 'CM_ID']
            s3.download_file('keep-truckin-production', f"uploads/camera_media/media/{cm_id}/{vid_filename}", os.path.join(videos_dl_dir, vid_filename))
        except Exception as e:
            error_index.append(i)
    for i in error_index:
        print(df['OFFLINE_ID'][i])
