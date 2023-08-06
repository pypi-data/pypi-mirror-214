<h1 align="center">OsmChange-generator-cli</h1>
<p align="center"><a href="https://www.openstreetmap.org/user/kwiatek_123)">Me on OpenStreetMap</a></p>

OsmChange file generator useful for importing and updating data in OpenStreetMap.

In its current phase of development, the generator does not support relations. Data files must be in `.geojson` format.

# Installation
```
pip install osmchange-generator-cli
```

# Usage

```
osmchange-generator \<input-file-names> \<osm-data-file-name> <out-file-name> <tag> (--log) (--create) (--delete) (--changeset-id)
```
## Help command with all arguments
```
osmchange-generator --help
```
## Example
```
osmchange-generator input_file.geojson osm_data.geojson out.osc ref --create --delete
```
(See `example` for generated file)