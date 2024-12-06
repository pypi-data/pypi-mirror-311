from minipath import MiniPath
import pandas as pd
from time import time
import logging
from PIL import Image

logging.getLogger()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Customize the format
)


low_mag = 'https://healthcare.googleapis.com/v1/projects/ml-mps-adl-dpp-ndsa-p-4863/locations/us/datasets/ml-phi-pathology-data-us-p/dicomStores/ml-phi-pathology-data-us-p-dicom-ndsa/dicomWeb/studies/1.2.840.113713.1.3593.593651.93651541/series/1.2.826.0.1.3680043.10.559.1139827362845547042694621547876929644/instances/1.3.6.1.4.1.11129.5.7.1.1.512983661164.78506680.1679804872800702'
high_mag = 'https://healthcare.googleapis.com/v1/projects/ml-mps-adl-dpp-ndsa-p-4863/locations/us/datasets/ml-phi-pathology-data-us-p/dicomStores/ml-phi-pathology-data-us-p-dicom-ndsa/dicomWeb/studies/1.2.840.113713.1.3593.593651.93651541/series/1.2.826.0.1.3680043.10.559.1139827362845547042694621547876929644/instances/1.2.826.0.1.3680043.10.559.8993976010537579281141045498595556829'


# Creating a pandas dataframe with the specified columns and dummy values
data = {
    "gcs_url": [
        low_mag,
        high_mag

    ],
    "SeriesInstanceUID": [low_mag.split('/')[16],
                          high_mag.split('/')[16]],
    "row_num_asc": [1, 2],
    "row_num_desc": [2, 1]
}
df = pd.DataFrame(data)
df.to_csv('test.csv', index=False)
start = time()
minipath = MiniPath(csv='test.csv', subset=True, patch_size=8, min_k=5, patch_per_cluster=1, max_k=2)
minipath.get_representatives(full_url=low_mag)
rep_time = time()
high_res_frames = minipath.get_high_res()
high_res_time = time()

i = 0
for x in high_res_frames:
   i = i + 1
   if x is None:
       continue
   img = Image.fromarray(x)
   img.save(f'test/{i}.png')


loop_time = time()

print(f'{i} patches,'
      f'Rep time: {(rep_time - start) / 60 :.2f} min, '
      f'HighRes: {(high_res_time - rep_time) / 60 :.2f} min, '
      f'Loop Time: {(loop_time-high_res_time) / 60 :.2f} min, '
      f'Total: {(loop_time - start) / 60 :.2f} min')
