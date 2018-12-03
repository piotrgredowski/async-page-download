# **Check status of the job**

Allows you to check status of registered job.

- **URL**

  `/api/jobs/JOB_UUID/status`

- **Method:**

  `GET`

- **URL Params**

  **Optional:**

  - `debug=1`

    When set, succesful request will return link to download results of job.

- **Success Response:**

  - **Code:** 200

    **Content:**

    ```json
    {
      "meta": {
        "imgs": {
          "done": 75,
          "failed": 0,
          "total": 75
        }
      },
      "status": "finished",
      "next_url": "http://localhost:8191/api/jobs/JOB_UUID"
    }
    ```

    Field `meta` contains information about status of downloaded images.

    Field `status` can be `started`, `queued`, `failed` or `finished`.

    Field `next_url` contains link to download results of job. (**ONLY IF `debug=1` IN PARAMS**)

- **Error Responses:**

  - **Code:** 404 NOT FOUND

    **Content:**

    ```json
    {
      "error": "There is no job with given ID"
    }
    ```

- **Sample Call:**

  ```bash
  curl -X GET \
    'http://localhost:8191/api/jobs/JOB_UUID/status?debug=1'
  ```
