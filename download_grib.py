import os
import requests
import gzip
import shutil
import subprocess
import xarray as xr
from datetime import datetime

# Configuration
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
file_url = 'https://mrms.ncep.noaa.gov/data/2D/MergedReflectivityAtLowestAltitude/MRMS_MergedReflectivityAtLowestAltitude.latest.grib2.gz'
local_directory = '/Users/trevorwiebe/Ktor/radar_backend/radar_data/grib_files'
csv_directory = '/Users/trevorwiebe/Ktor/radar_backend/radar_data/csv_files'

compressed_file_path = os.path.join(local_directory, 'MRMS_MergedReflectivityAtLowestAltitude.latest.grib2.gz')
decompressed_file_path = os.path.join(local_directory, f'{current_time}.grib2')
cropped_grib_file = os.path.join(local_directory, f'{current_time}_cropped.grib2')
idx_cropped_grib_file = os.path.join(local_directory, f'{current_time}_cropped.grib2.9093e.idx')
csv_file = os.path.join(csv_directory, f'{current_time}_cropped.csv')

# Ensure the local directory exists
os.makedirs(local_directory, exist_ok=True)

def download_file(url, compressed_file_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(compressed_file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded {url} to {compressed_file_path}")

def decompress_file(compressed_path, decompressed_path):
    with gzip.open(compressed_path, 'rb') as f_in:
        with open(decompressed_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Decompressed {compressed_path} to {decompressed_path}")

def crop_grib(input_file, output_file, left_long, right_long, top_lat, bottom_lat):
    # Format the command and arguments
    command = [
        "cdo",
        f"sellonlatbox,{left_long},{right_long},{top_lat},{bottom_lat}",
        input_file,
        output_file
    ]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Return the output or error
    if result.returncode == 0:
        return f"Command executed successfully\nOutput: {result.stdout}"
    else:
        return f"Error: {result.stderr}"

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"File {file_path} does not exists, so it could not be deleted.")

def output_to_csv(grib_file):
    ds = xr.open_dataset(grib_file, engine='cfgrib')
    df = ds.to_dataframe().reset_index()
    df.to_csv(csv_file, index=False)


def main():
    try:
        if not os.path.exists(compressed_file_path):
            download_file(file_url, compressed_file_path)
        else:
            print(f"The file {compressed_file_path} is already downloaded.")

        if not os.path.exists(decompressed_file_path):
            decompress_file(compressed_file_path, decompressed_file_path)
            crop_grib(decompressed_file_path, cropped_grib_file, -101.25, -95.625, 40.9799, 36.59789)
            output_to_csv(cropped_grib_file)
            delete_file(compressed_file_path)
            delete_file(decompressed_file_path)
            delete_file(idx_cropped_grib_file)
        else:
            print(f"The decompressed file {decompressed_file_path} already exists.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
