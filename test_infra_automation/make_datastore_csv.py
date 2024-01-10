import pandas as pd
import json
import argparse

def read_csv_file(input_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_path)
    return df

if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Read CSV file into a Pandas DataFrame and add additional data.')

    # Add arguments for the input and output file paths
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to the input CSV file.')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to the output CSV file.')
    # Parse the arguments
    args = parser.parse_args()

    # Read the CSV file
    dataframe = read_csv_file(args.input)  
    dataframe.columns = dataframe.columns.str.lower()

    # Define the column names
    column_names = [
        "offline_id", "cm_id", "camera_face", "source_type", "fps", "width", "height", 
        "added_by", "tags", "cam_init_source", "cam_init_model_version", "cam_init_model_type", 
        "gt_close_following", "gt_mobile_usage", "gt_seatbelt", "gt_distraction", 
        "gt_unsafe_lane_change", "cam_init_params", "skip_motion_data", "overwrite", 
        "gt_camera_obstruction", "gt_forward_collision_warning","gt_rolling_stop"
    ]

    with open('/home/muhammadasadsoomro/Desktop/Work/test_infra_automation/config.json', 'r') as file:
        data_store_configs = json.load(file)

    # Create an empty DataFrame with the specified column names
    empty_df = pd.DataFrame(columns=column_names)

    # making the final df 
    empty_df['offline_id'] = dataframe['offline_id']
    empty_df['cm_id'] = dataframe['cm_id']
    
    # adding all the data from the json file
    for key , value in data_store_configs.items():
        empty_df[key] = value
    
    # if the columns starting if the gt exist in the dataframe then add value from the dataframe to the empty_df else keep it empty
    for c in ["gt_close_following", "gt_mobile_usage", "gt_seatbelt", "gt_distraction", "gt_unsafe_lane_change", "cam_init_params", "skip_motion_data", "overwrite", "gt_camera_obstruction", "gt_forward_collision_warning","gt_rolling_stop"]:
        if c in dataframe.columns.tolist():
            empty_df[c] = dataframe[c]
        else:
            continue
    empty_df = empty_df[column_names]
    # Optionally, save the DataFrame to a new CSV file
    empty_df.to_csv(args.output, index=False)
