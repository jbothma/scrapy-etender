# scrapy-etender

Scrape a snapshot of the eTender portal.

This doesn't try to track a tender process's status - it simply scrapes the data as it is currently presented on the eTender portal.

Something can then use these snapshots to deduce the progression of a tender process over time.

This should ideally be run daily, archiving the snapshots somewhere reliable.


## Production

For production deployment, this can easily be run in Scrapinghub, scrapyd or from the command line similarly to development.

**requirements.txt is the authoritative dependency file so that scraipinghub can install dependencies.**


### Exporting to the Internet Archive:

Use the Feed Exporter configuration with the `internetarchive` URI scheme.

The Internet Archive feed exporter should have the hostname `archive.org`, Internet Archive S3 API access key and secret in the username and password positions.

Only one level of path is allowed. This will be used as the filename, and will be transformed into a unique identifier, meaning it should be unique on all of the Internet Archive. Including the scrape job timestamp in this path is useful for ensuring uniqueness.

Extra parameters can be provided as query string parameters, which will then be templated into the metadata values.

Metadata values can be specified using the settings key `FEED_STORAGE_INTERNETARCHIVE`, e.g.

```
FEED_STORAGE_INTERNETARCHIVE = {
    "metadata": {
        "mediatype": "data",
        "coverage": "South Africa",
        "title": "eTender Portal %(name)s %(time)s",
    }
}
```

You probably don't want to put credentials into your project settings module, since it can then easily be discovered if added to source control.

You can set the `FEEDS` key in scrapinghub by providing the value dictionary as JSON on a single line in your spider's Raw Settings. e.g. for the following setting:

```
FEEDS = {
    "internetarchive://YourIAS3AccessKeyYourIAS3AccessKey:YourIAS3APISecretKey@archive.org/south-africa-%(name)s-%(time)s.csv?time=%(time)s&name=%(name)s": {
        "format": "csv",
    },
    "internetarchive://YourIAS3AccessKey:YourIAS3APISecretKey@archive.org/south-africa-%(name)s-%(time)s.jsonlines?time=%(time)s&name=%(name)s": {
        "format": "jsonlines",
    },
}
```

add the following line in the scrapinghub Raw settings:

```
FEEDS = {"internetarchive://YourIAS3AccessKey:YourIAS3APISecretKey@archive.org/south-africa-%(name)s-%(time)s.csv?time=%(time)s&name=%(name)s": {"format": "csv"}, "internetarchive://YourIAS3AccessKey:YourIAS3APISecretKey@archive.org/south-africa-%(name)s-%(time)s.jsonlines?time=%(time)s&name=%(name)s": { "format": "jsonlines" }}
```

After saving, you should see it parsed into a key and value on the standard settings pane.


## Development

Install dependencies

    pipenv install

Run the advertised tenders scraper

    pipenv run scrapy crawl advertised-tenders -t csv -o advertised-tenders.csv

Run the awarded tenders scraper

    pipenv run scrapy crawl awarded-tenders -t csv -o awarded-tenders.csv
