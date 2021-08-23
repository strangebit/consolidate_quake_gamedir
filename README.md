# consolidate_quake_gamedir

This Python script will consolidate a Quake gamedir with loose files and PAKs into a single PAK file.

## Usage

Command-line usage: `python -m consolidate_quake_gamedir [--quiet | --verbose] gamedir`  

Or from a Python script:

```python
from consolidate_quake_gamedir import consolidate, PrintOut

# PrintOut.NONE
# PrintOut.INFO (default if not specified)
# PrintOut.VERBOSE
consolidate('gamedir', PrintOut.INFO)
```

Outputs: `gamedir_consolidated/pak0.pak`

Example console output:
```
Unpaking gamedir/pak0.pak to gamedir_temp
Unpaking gamedir/pak1.pak to gamedir_temp
Unpaking gamedir/pak2.pak to gamedir_temp
Copying free files from gamedir to gamedir_temp
Repaking gamedir_temp to gamedir_consolidated/pak0.pak
Cleaning up temporary files from gamedir_temp
```

## Dependency

[vgio](https://github.com/joshuaskelly/vgio)  
Install with: `pip install vgio`

## Simple example
Run `python -m example.consolidate_hwjam3` from the root folder

This example script will automatically download [Halloween Jam 3](https://www.quaddicted.com/reviews/hwjam3.html),
extract it to `hwjam3`, and consolidate it to `hwjam3_consolidated/pak0.pak`. This all
happens within the `example` subdirectory.

## LICENSE
[CC0 1.0 Universal](LICENSE)
