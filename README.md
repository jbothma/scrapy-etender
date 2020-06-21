# scrapy-etender

## Production

For production deployment, this can easily be run in Scrapinghub, scrapyd or from the command line similarly to development.

**requirements.txt is the authoritative dependency file so that scraipinghub can install dependencies.**


## Development

Install dependencies

    pipenv install

Run the advertised tenders scraper

    pipenv run scrapy crawl advertised-tenders -t csv -o advertised-tenders.csv

Run the awarded tenders scraper

    pipenv run scrapy crawl awarded-tenders -t csv -o awarded-tenders.csv
