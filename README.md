# OSM polygons extractor #

Memory efficient Open Street Map (OSM) data converter to shp files.
It may be used to extract polygon layers that exists in OSM database
but are not extracted other way.


## Requirements ##

 * Python 2.7 (should work with earlier versions also)
 * pyshp 1.2.0


## Usage ##

    usage: osmpolygons [-h] [--filter FILTER] [--include-tags META_KEYS]
                       [--no-cache] [--out OUT]
                       [input]

    positional arguments:
      input

    optional arguments:
      -h, --help            show this help message and exit
      --filter FILTER, -f FILTER
                            comma separated k=v pairs of relation tag filters
      --include-tags META_KEYS, -i META_KEYS
                            comma separated list of tag names to be extracted as
                            meta data
      --no-cache            disable partial results caches
      --out OUT, -o OUT     output file name (without extension)


## Features ##

None of available tools I've seen does extract filtered polygons data from OSM.
In Poland there is layer of powiats (administrative unit), that is not extracted
in accessible [datasets](http://download.geofabric.de) in shp format.

You may set different set of filters to grab any polygons layer you want


## TODO ##

- [ ] Add osm pbf format handling (it's faster to process this than xml)
- [ ] Add optional dumps to json
- [ ] Add optional dumps to simple xml
- [ ] Add optional dumps to pickled tuples (metadatadict, [polylines])
