import zipfile
import os
from tempfile import NamedTemporaryFile


def change_temp_filename(src_name, dest_name):
    splitted = src_name.split("/")
    splitted[-1] = dest_name
    return "/".join(splitted)


def remove_file(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass


class Page:
    "Represents downloaded page with its url, text and images"

    def __init__(self, url, text, imgs):
        self._url = url
        self._text = text
        self._imgs = imgs
        self.temp_filenames = []

        self.zipped_filename = None

    @property
    def url(self):
        return self._url

    @property
    def text(self):
        return self._text

    @property
    def imgs(self):
        return self._imgs

    def _save_to_file(self, content, filename, mode="w+b"):
        with NamedTemporaryFile(mode=mode, delete=False) as temp_file:
            temp_file.write(content)

            new_filename = change_temp_filename(temp_file.name, filename)
            os.rename(temp_file.name, new_filename)

            self.temp_filenames.append(new_filename)

    def _save_all_files(self, filename):
        self._save_to_file(self._text, filename + ".txt", mode="w+t")
        for img in self._imgs:
            self._save_to_file(img["img"], img["name"])

    def save_to_zip(self, filename):
        """
        Saves text and images from page to ZIP archive.

        Args:
            filename (str): name of text file

        Returns:
            str: name of created ZIP file
        """
        self._save_all_files(filename)

        with NamedTemporaryFile(delete=False) as temp_zip_file:
            with zipfile.ZipFile(file=temp_zip_file,
                                 mode="w",
                                 compression=zipfile.ZIP_DEFLATED) as archive:
                for temp_filename in self.temp_filenames:
                    archive.write(temp_filename)
            self.zipped_filename = temp_zip_file.name
            return self.zipped_filename

    def remove_created_files(self):
        "Removes all files created during saving page to ZIP archive."
        remove_file(self.zipped_filename)
        for filename in self.temp_filenames:
            remove_file(filename)
