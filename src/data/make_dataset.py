import subprocess
from kaggle.api import KaggleApi
from zipfile import ZipFile
import os
import yaml

CONFIG_FILE = 'config.yaml'
def download_dataset():
    """ Download and extract the Kaggle MNIST dataset.
    """
    with open(CONFIG_FILE) as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    competition = config['data']['kaggle']['competition']
    files = config['data']['kaggle']['files']
    output_dir = config["data"]["raw_folder"]

    api = KaggleApi()
    api.authenticate()

    for d in files.values():
        subprocess.run(
            [
                "kaggle",
                "competitions",
                "download",
                f"{competition}",
                "-f"
                f"{d}",
                "--path",
                f"{output_dir}",
            ],
            check=True,
        )

        with ZipFile(f'{output_dir}/{d}.zip', 'r') as zipObj:
            zipObj.extractall(f'{output_dir}')

        try:
            os.remove(f'{output_dir}/{d}.zip')
        except exc:
            print(exc)

if __name__ == "__main__":
    download_dataset()