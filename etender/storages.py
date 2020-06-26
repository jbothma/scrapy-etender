from scrapy.extensions.feedexport import BlockingFeedStorage
from urllib.parse import unquote, urlparse, parse_qs
from internetarchive import upload
from scrapy.utils.project import get_project_settings
import re


class InternetArchiveStorage(BlockingFeedStorage):

    def __init__(self, uri, use_active_mode=False):
        u = urlparse(uri)
        self.host = u.hostname
        self.username = u.username
        self.password = unquote(u.password)
        paths = u.path.split("/")
        assert(len(paths) == 2)
        root_path = paths[1]
        self.identifier = re.sub("[^\\w_-]+", "_", root_path)
        self.filename = root_path

        settings = get_project_settings()
        unformatted_metadata = settings["FEED_STORAGE_INTERNETARCHIVE"]["metadata"]
        self.scrape_params = {}
        for key, value in parse_qs(u.query).items():
            self.scrape_params[key] = value[0]
        self.metadata = {}
        for key, value in unformatted_metadata.items():
            self.metadata[key] = value % self.scrape_params

    def _store_in_thread(self, file):
        file.seek(0)
        upload(
            self.identifier,
            files={self.filename: file},
            metadata=self.metadata,
            access_key=self.username,
            secret_key=self.password,
        )
