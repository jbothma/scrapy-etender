# scrapy-etender

Scrape a snapshot of the eTender portal.

This doesn't try to track a tender process's status - it simply scrapes the data as it is currently presented on the eTender portal.

Something can then use these snapshots to deduce the progression of a tender process over time.

This should ideally be run daily, archiving the snapshots somewhere reliable.


## Production

For production deployment, this can easily be run in Scrapinghub, scrapyd or from the command line similarly to development.

**requirements.txt is the authoritative dependency file so that scraipinghub can install dependencies.**


### Exporting to the Internet Archive:

Uses [scrapy-feed-storage-internetarchive](https://github.com/OpenUpSA/scrapy-feed-storage-internetarchive) to archive items to archive.org.

Enable using the `internetarchive` scheme in `FEEDS` e.g.

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


## Development

Install dependencies

    pipenv install

Run the advertised tenders scraper

    pipenv run scrapy crawl advertised-tenders -t csv -o advertised-tenders.csv

Run the awarded tenders scraper

    pipenv run scrapy crawl awarded-tenders -t csv -o awarded-tenders.csv
