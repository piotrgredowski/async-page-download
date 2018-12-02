import urllib.request
from urllib.parse import urlparse
from urllib.error import HTTPError

from bs4 import BeautifulSoup
from rq import get_current_job

from utils import log


class Downloader:
    "Handles downloading page content and images."

    def __init__(self):
        self.scheme = None
        self.netloc = None

        self.no_of_imgs = 0

    def _extract_url(self, url):
        parsed_url = urlparse(url)
        self.scheme = parsed_url.scheme
        self.netloc = parsed_url.netloc

    def _get_url_content(self, url, timeout=5):
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return response.read()

    def _get_urls_of_imgs(self, soup):
        imgs = soup.find_all("img")
        return [img["src"] for img in imgs]

    def _get_correct_url(self, url):
        parsed_img_url = urlparse(url)
        if not parsed_img_url.scheme:
            parsed_img_url = parsed_img_url._replace(scheme=self.scheme)
        if not parsed_img_url.netloc:
            parsed_img_url = parsed_img_url._replace(netloc=self.netloc)

        return parsed_img_url.geturl()

    def _get_img_name_from_url(self, url):
        parsed_url = urlparse(url)
        path = parsed_url.path

        return path.split("/")[-1]

    # TODO: It is breaking SRP. Think about how to do it better.
    def _update_meta_of_job(self, no_of_done, no_of_failed):
        cur_job = get_current_job()
        if not cur_job:
            return
        cur_job.meta.update({"imgs": {"done": no_of_done,
                                      "failed": no_of_failed,
                                      "total": self.no_of_imgs}})
        cur_job.save_meta()

    def _get_imgs_with_names(self, soup):
        urls = self._get_urls_of_imgs(soup)
        self.no_of_imgs = len(urls)

        no_of_failed = 0
        no_of_successed = 0
        imgs = []

        for url in urls:
            url = self._get_correct_url(url)
            try:
                img = self._get_url_content(url)
            except TimeoutError:
                log.error("Timeout exceeded on %s", url)
                no_of_failed += 1
            except HTTPError:
                log.error("Error while opening %s", url)
                no_of_failed += 1
            else:
                imgs.append({"img": img, "name": self._get_img_name_from_url(url)})
                log.info("Image downloaded from %s", url)
                no_of_successed += 1
            finally:
                self._update_meta_of_job(no_of_successed, no_of_failed)

        return imgs

    def _convert_text(self, text):
        # Break into lines and remove trailing whitespace
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip()
                  for line in lines
                  for phrase in line.split("  "))
        # Remove blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def _get_text(self, soup):
        # Remove CSS & JS
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text()
        text = self._convert_text(text)
        return text

    def get_page(self, url):
        """
        Returns instance of Page with downloaded text and images.

        Args:
            url (str)

        Returns Page
        """

        self._extract_url(url)

        html = self._get_url_content(url)
        soup = BeautifulSoup(html, "html.parser")

        imgs = self._get_imgs_with_names(soup)
        text = self._get_text(soup)
        from page_handling import Page

        return Page(url, text, imgs)
