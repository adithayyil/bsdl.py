# bsdl
## 🛠️ WIP

#### Inspired by [scdl](https://github.com/flyingrub/scdl) & [ttdl](https://github.com/claydol/ttdl)

## Installation
```
python3 setup.py install
```

## Usage

#### Download all tracks from a artist
```
bsdl -a [ARTIST]
```
#### Download a track
```
bsdl -t [LINK]
```

## To-Do

- [x] Find out why agolia only retreving 100 sets per request ([Read](https://www.algolia.com/doc/guides/managing-results/refine-results/faceting/))
- [x] Get track titles
- [ ] Download a single track from a link/trackID
- [ ] Loop through each [page](https://www.algolia.com/doc/api-reference/api-parameters/page/) if there are 100> tracks
- [ ] Depoly to PyPi
