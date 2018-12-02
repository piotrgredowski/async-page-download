import unittest
from unittest.mock import (
    MagicMock,
    patch,
)
import json
import uuid

from fakeredis import FakeStrictRedis
from rq import Queue

from serve import make_app
import page_handling


MOCKED_GET_PAGE = "Example page."


def mock_get_page(url, text="", imgs=None):
    if imgs is None:
        imgs = {}
    return page_handling.Page(url=url, text=text, imgs=imgs)


class TestViews(unittest.TestCase):

    def setUp(self):
        self.queue = Queue(name="fake_queue", is_async=False,
                           connection=FakeStrictRedis())

        self.app = make_app("config.yml")
        self.app.queue = Queue(name="fake_queue", is_async=False,
                               connection=FakeStrictRedis())
        self.app.config['TESTING'] = True

        self.client = self.app.test_client()

    def test_register_job(self):
        "Test successful job register"
        # Needed for getting result_ttl inside register_job function
        self.app.cfg.get = MagicMock(return_value=-1)

        with patch("page_handling.Downloader._get_url_content",
                   return_value=MOCKED_GET_PAGE):
            ret = self.client.put("/api/jobs",
                                  data=json.dumps({"url": "http://faked-site.dev"}),
                                  content_type='application/json')
        self.assertEqual(ret.status_code, 200)

        ret_json = ret.get_json()

        self.assertIsInstance(ret_json, dict)
        self.assertIn("job_id", ret_json)
        self.assertIsInstance(uuid.UUID(ret_json["job_id"]), uuid.UUID)

    def test_register_job_failing(self):
        "Test failing job register"
        with patch("page_handling.Downloader._get_url_content",
                   return_value=MOCKED_GET_PAGE):
            ret = self.client.put("/api/jobs",
                                  data=json.dumps({"wrong_key": "value"}),
                                  content_type='application/json')

        self.assertEqual(ret.status_code, 400)

    def test_check_status_of_job(self):
        "Test checking status of job"

        with self.app.app_context():
            url = ""
            job = self.app.queue.enqueue(mock_get_page, args=(url,))

            expected_status = "finished"
            assert expected_status == job.get_status()

            ret = self.client.get("/api/jobs/{}/status".format(job.id))

        ret_json = ret.get_json()

        self.assertEqual(ret.status_code, 200)
        self.assertIn("status", ret_json)
        self.assertEqual(ret_json["status"], expected_status)

    def test_check_status_of_non_existing_job(self):
        "Test checking status of non existing job"
        non_existing_job_id = uuid.uuid4()
        with self.app.app_context():
            assert non_existing_job_id not in self.app.queue.get_job_ids()

            ret = self.client.get("/api/jobs/{}/status".format(non_existing_job_id))

        ret_json = ret.get_json()
        self.assertEqual(ret.status_code, 404)
        self.assertEqual(ret_json, "There is no job with given ID")

    def test_get_result_of_job(self):
        "Test getting result of job"
        exp_url = "http://fake.dev"
        exp_text = "Text."

        with self.app.app_context():
            job = self.app.queue.enqueue(mock_get_page, args=(exp_url, exp_text))

            ret = self.client.get("/api/jobs/{}".format(job.id))

        ret_data = ret.data

        self.assertEqual(ret.status_code, 200)
        self.assertIsInstance(ret_data, bytes)

    def test_get_result_of_non_existing_job(self):
        "Test getting result of non existing job"
        non_existing_job_id = uuid.uuid4()

        with self.app.app_context():
            assert non_existing_job_id not in self.app.queue.get_job_ids()

            ret = self.client.get("/api/jobs/{}".format(non_existing_job_id))

        ret_json = ret.get_json()
        self.assertEqual(ret.status_code, 404)
        self.assertEqual(ret_json, "There is no job with given ID")
