# scrapy-etender


## Development

Install dependencies

    pipenv install

Run the advertised tenders scraper

    pipenv run scrapy crawl advertised-tenders -t csv -o advertised-tenders.csv

Run the awarded tenders scraper

    pipenv run scrapy crawl awarded-tenders -t csv -o awarded-tenders.csv
