# foxplot

[![Build](https://img.shields.io/github/actions/workflow/status/stephane-caron/foxplot/CI.yml?branch=main)](https://github.com/stephane-caron/foxplot/actions)

Plot time-series data from [line-delimited JSON](https://en.wikipedia.org/wiki/JSON_streaming#Line-delimited_JSON):

## Usage

### JSON files

```console
$ foxplot my_time_series.json
```

### MessagePack files

```console
rq -mJ < my_time_series.mpack | jq '{.my.filters.here}' | foxplot
```

## See also

* [µPlot](https://github.com/leeoniya/uPlot)'s performance was a key enabler for this project.
* [rq](https://github.com/dflemstr/rq/), a tool to manipulate streams of records in various formats.
