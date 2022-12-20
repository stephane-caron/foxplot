# foxplot

Plot time-series data from [line-delimited JSON](https://en.wikipedia.org/wiki/JSON_streaming#Line-delimited_JSON):

```console
rq -mJ < my_log.mpack | jq '{...}' | foxplot -x time
```

## Acknowledgements

* [µPlot](https://github.com/leeoniya/uPlot)'s performance was a key enabler for this project.
