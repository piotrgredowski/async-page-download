# **Get results of the job**

Allows you to download results of registered job.

- **URL**

  `/api/jobs/JOB_UUID`

- **Method:**

  `GET`

- **URL Params**

  **Optional:**

  - `delete_after_download=1`

    When set, successful job will be deleted.

- **Success Response:**

  - **Code:** 200

    **Content:** ZIP file with extracted text and images.

- **Error Responses:**

  - **Code:** 404 NOT FOUND

    **Content:**

    ```json
    {
      "error": "There is no job with given ID"
    }
    ```

    OR

  - **Code:** 409 CONFLICT

    **Content:**

    ```json
    {
      "error": "Job failed."
    }
    ```

    OR

  - **Code:** 409 CONFLICT

    **Content:**

    ```json
    {
      "error": "Job is not finished, try again later."
    }
    ```

* **Sample Call:**

  ```bash
  curl -X GET \
    'http://localhost:8191/api/jobs/JOB_UUID' \
    -O -J
  ```
