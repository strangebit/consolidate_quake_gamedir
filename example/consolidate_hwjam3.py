# Downloads Halloween Jam 3 (hwjam3.zip), extracts it, and consolidates it.
# All happens within the example subdirectory.
#
# Command-line usage (from root dir): python -m example.consolidate_hwjam3

import os
import shutil
import requests
from zipfile import ZipFile

from consolidate_quake_gamedir import consolidate, PrintOut

mod = 'hwjam3'
mod_name = "Halloween Jam 3"
mod_zip = mod + ".zip"
mod_url = 'https://www.quaddicted.com/filebase/' + mod_zip

def download_mod():
    if not os.path.isfile(mod_zip):
        print(f'{mod_name} ({mod_zip}) not found.')
        print(f'Downloading {mod_name} from: {mod_url}')
        print('  Please wait; this may take a while...')
        r = requests.get(mod_url)
        open(mod_zip, 'wb').write(r.content)

def extract_mod():
    print(f'Deleting any existing {mod} gamedir')
    shutil.rmtree(mod, True)

    print(f'Extracting {mod_name} ({mod_zip}) to {mod} gamedir')
    with ZipFile(mod_zip, 'r') as zipObj:
        zipObj.extractall(mod)

def consolidate_mod():
    consolidate(mod, PrintOut.VERBOSE)

if __name__ == '__main__':
    # Change current dir to example subdir
    os.chdir(os.path.dirname(__file__))

    download_mod()
    extract_mod()
    consolidate_mod()
