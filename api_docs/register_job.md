# **Register job**

Allows you to register a job with given URL.

- **URL**

  `/api/jobs`

- **Method:**

  `PUT`

- **URL Params**

  **Optional:**

  - `debug=1`

    When set, succesful request will return link to check status of job.

- **Data Params**

  ```json
  {
    "url": "https://en.wikipedia.org/wiki/World_War_II"
  }
  ```

- **Success Response:**

  - **Code:** 200

    **Content:**

    ```json
    {
      "job_id": "JOB_UUID",
      "next_url": "http://localhost:8191/api/jobs/JOB_UUID/status?debug=1"
    }
    ```

- **Error Response:**

  - **Code:** 400 BAD REQUEST

    **Content:**

    ```json
    {
      "error": "No 'url' in request body"
    }
    ```

- **Sample Call:**

  ```bash
  curl -X PUT \
    'http://localhost:8191/api/jobs?debug=1' \
    -H 'Content-Type: application/json' \
    -d '{"url": "https://en.wikipedia.org/wiki/World_War_II"}'
  ```
