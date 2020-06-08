# Stitch OpenStreetMap tiles

### PURPOSE

This python program stitches  OSM(OpenStreetMap) titles.

The tiles directory format will be image_type/horizontal/vertical.

The program stitches 10,000 tiles and the size of the tiles varies.

 
### INPUT / OUTPUT

Input is osm tiles directory name.

If input is omitted, this program searches its own directory to stitch.

Output are stitched files in the new directory.


### REQUIREMENT

Required packages: Pillow, xmltodict


### HOW TO RUN

```
python stitch_osm_tiles.py

python stitch_osm_tiles.py --dirname test-data
```
