# foxplot

[![Build](https://img.shields.io/github/actions/workflow/status/stephane-caron/foxplot/CI.yml?branch=main)](https://github.com/stephane-caron/foxplot/actions)

Plot time-series data from [line-delimited JSON](https://en.wikipedia.org/wiki/JSON_streaming#Line-delimited_JSON).

Foxplot stands for "Frequent Observation diXionary plots". Frequent observations arise from the project's initial use case (robotic control loops). Dictionaries are the observation format used in [Vulp](https://github.com/tasts-robots/vulp). Plots are plots :wink:

## Usage

### Interactive mode

```console
$ foxplot -i robot_data.json
Python 3.8.10 (default, Mar 13 2023, 10:26:41)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.22.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: fox.plot(left=[fox.data.observation.cpu_temperature])
New tab opened in your web browser! The command line is to produce it directly is:

foxplot robot_data.json -l /observation/cpu_temperature
```

### JSON files

```console
foxplot robot_data.json -l /observation/cpu_temperature
```

### MessagePack files

```console
rq -mJ < my_time_series.mpack | jq '{.my.filters.here}' | foxplot
```

## Design notes

* Foxplot prioritizes ease-of-use (interactive mode) over performance

## See also

* [µPlot](https://github.com/leeoniya/uPlot)'s performance was a key enabler for this project.
* [rq](https://github.com/dflemstr/rq/), a tool to manipulate streams of records in various formats.
