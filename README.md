# cdf-scrapers

This is a library of scrapers for producing easy-to-consume JSON files of information for [CDF](http://www.cdf.toronto.edu/) services.


## Library Reference

### Lab machine availability

##### Data
<http://www.cdf.toronto.edu/~g3cheunh/cdflabs.json>

##### Scraper source
<http://www.cdf.toronto.edu/usage/usage.html>

##### Output format
```js
{
    "labs": [{
        "name": String,
        "available": Number,
        "busy": Number,
        "total": Number,
        "percent": Number,
        "timestamp": String
    }]
}
```

------

### Printer job queues

##### Data
<http://www.cdf.toronto.edu/~g3cheunh/cdfprinters.json>

Old format: <http://www.cdf.toronto.edu/~g3cheunh/printdata.json>

##### Scraper source
Output of the `lpq -a` command on a CDF machine.

##### Output format
```js
{
    "printers": {
        name: {
            "name": String,
            "description": String,
            "length": Number
            "jobs": [{
                "rank": String,
                "owner": String,
                "class": String,
                "job": String,
                "files": String,
                "size": String,
                "time": String
            }]
        }
    }
    "timestamp": String
}
```

------

#### Running on CDF

The scripts are currently being run every minute via a Cron job on a CDF machine:

```
* * * * * /h/u10/g3/00/g3cheunh/cdf-scrapers/lpq.sh
```
