# cdf-scrapers

This is a library of scrapers for producing easy-to-consume JSON files of information for [CDF](http://www.cdf.toronto.edu/) services.


## Library Reference

### Lab machine availability
**Coming soon**

##### Scraper source
<http://www.cdf.toronto.edu/usage/usage.html>

##### Output format
Not implemented.

------

### Printer job queues

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

Cron job:
```
* * * * * /h/u10/g3/00/g3cheunh/cdf-printdata/lpq.sh
```

JSON file available here: <http://www.cdf.toronto.edu/~g3cheunh/cdfprinters.json>

Old format file: <http://www.cdf.toronto.edu/~g3cheunh/printdata.json>
