# ALTLinux RDB Compare

## Setup

```
$ python3 -m venv .venv && source ./.venv/bin/activate
```

```
$ pip install -r requirements.txt
```

## Usage:

Help:
```shell
./rdb-compare -h
```

Compare all arches:
```shell
./rdb-compare sisyphus p10 > res.json
```

Compare only selected arches:
```shell
./rdb-compare sisyphus p10 --arch noarch aarch64 > res.json
```

### Result format

```json
{
    "[arch_1]": {
        "missing": {
            "first": [
                "[foo]",
                "[bar]",
                ...
            ]
            "second": [
                "[baz]",
                ...
            ]
        },
        "newer": {
            "first": [
                {
                    "name": "[qux]",
                    "first": {
                        "version": "[version_from_first]",
                        "epoch": [epoch_from_first]
                    },
                    "second": {
                        "version": "[version_from_second]",
                        "epoch": [epoch_from_second]
                    }
                },
                ...
            ]
        }
    },
    ...
}
```