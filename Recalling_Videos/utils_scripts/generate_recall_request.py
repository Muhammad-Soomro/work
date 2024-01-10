import sys
import os
import csv
import argparse
from csv import DictReader
from io import TextIOWrapper

import requests


def main(file):
    os.environ["cam_prod_key"] = 'TFpmKLsjnGbQYYwbFX5vggLgv0Rdft'
    headers = {"X-Internal-Api-Key": os.environ["cam_prod_key"]}
    admin_key = 3156
    reader = DictReader(TextIOWrapper(file, encoding='utf-8'), dialect='unix', quoting=csv.QUOTE_MINIMAL)
    writer = csv.writer(sys.stdout, dialect='unix', quoting=csv.QUOTE_MINIMAL)

    eld_count_map = {}
    writer.writerow(['RECORD_ID', 'ELD_ID', *reader.fieldnames])
    for row in reader:
        start_time = row['START_TIME'].split('.')[0].replace('T', ' ')
        #end_time = row['END_TIME'].split('.')[0].replace('T', ' ')
        vehicle_id = row['VEHICLE_ID']
        try:
            if  row['VEHICLE_ID'] not in eld_count_map:
                eld_count_map[row['VEHICLE_ID']] = 1


            # if eld_count_map[row['VEHICLE_ID']] > 1:
            #     continue

            response = requests.post('https://api.keeptruckin.com/api/i1/video_recall_requests',
                                     {
                                     "vehicle_id": vehicle_id,
                                     "admin_user_id": admin_key,
                                     "requested_start_time": start_time,
                                  },
                                     headers=headers)

            eld_count_map[row['VEHICLE_ID']] += 1
        except:
            continue
        
        try:
            request_response = response.json()['video_recall_request'][0]
            record_id = request_response['id']
            eld_id = request_response['eld_device_id']
        except KeyError:
            continue
        writer.writerow([record_id, eld_id, *list(row.values())])

    return


def _start():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='file', type=argparse.FileType('rb'))

    args = vars(parser.parse_args())
    file = args['file']
    file = sys.stdin.buffer if file is sys.stdin else file

    main(file)
    sys.exit()


if __name__ == '__main__':
    _start()
