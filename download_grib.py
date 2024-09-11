import os
import requests
import gzip
import shutil
import subprocess
import glob
import xarray as xr
from datetime import datetime, timezone

# Configuration
current_time = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H%M')
file_url = 'https://mrms.ncep.noaa.gov/data/2D/MergedReflectivityAtLowestAltitude/MRMS_MergedReflectivityAtLowestAltitude.latest.grib2.gz'
grib_directory = '/var/www/radar_data/grib_files'
csv_directory = '/var/www/radar_data/csv_files'

compressed_file_path = os.path.join(grib_directory, f'{current_time}.grib2.gz')
decompressed_file_path = os.path.join(grib_directory, f'{current_time}_decompressed.grib2')
cropped_grib_file = os.path.join(grib_directory, f'{current_time}_cropped.grib2')
idx_cropped_grib_file = os.path.join(grib_directory, f'{current_time}_cropped.grib2.9093e.idx')
csv_file = os.path.join(csv_directory, f'{current_time}_cropped.csv')

# Ensure the local directory exists
os.makedirs(grib_directory, exist_ok=True)

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

    # Construct the wgrib2 command
    command = [
        'wgrib2',
        input_file,
        '-small_grib',
        f'{left_long}:{right_long}',
        f'{bottom_lat}:{top_lat}',
        output_file
    ]

    cdo_command = [
        'cdo',
        'sellonlatbox,' + f'{left_long},{right_long},{bottom_lat},{top_lat}',
        input_file,
        output_file
    ]

    # Run the command
    try:
        result = subprocess.run(cdo_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f'Successfully cropped the GRIB2 file: {output_file}')
        print(result.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(f'Error occurred: {e.stderr.decode("utf-8")}')

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"File {file_path} does not exists, so it could not be deleted.")

def output_to_csv(grib_file):
    ds = xr.open_dataset(grib_file, engine='cfgrib')
    df = ds.to_dataframe().reset_index()
    df.to_csv(csv_file, index=False)

def delete_idx_files(directory_path):

    pattern = os.path.join(directory_path, '*.grib2.*.idx')

    # Find all files ending with .idx in the directory
    idx_files = glob.glob(pattern)

    # Loop through the list and delete each file
    for file_path in idx_files:
        os.remove(file_path)
        print(f"Deleted: {file_path}")

def main():
    try:
        if not os.path.exists(compressed_file_path):
            download_file(file_url, compressed_file_path)
        else:
            print(f"The file {compressed_file_path} is already downloaded.")

        if not os.path.exists(decompressed_file_path):
            decompress_file(compressed_file_path, decompressed_file_path)
            crop_grib(decompressed_file_path, cropped_grib_file, -95.45, -92.05, 31.05, 33.95)
            # crop_grib(decompressed_file_path, cropped_grib_file, -101.25, -95.625, 36.59789, 31.95216)
            output_to_csv(cropped_grib_file)
            delete_file(compressed_file_path)
            delete_file(cropped_grib_file)
            delete_idx_files(grib_directory)
        else:
            print(f"The decompressed file {decompressed_file_path} already exists.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
