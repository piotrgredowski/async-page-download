# ASYNC PAGE DOWNLOAD

## About

Application can be used to download asynchronously web pages. You can send URL to specified endpoint
and then check status of assigned job. Finally you can download ZIP archive containing extracted
text and images.

## Requirements

Application should be run with `docker-compose@1.23.1`.

## Usage

You can start application easily using (in root directory of project):

```bash
docker-compose up
```

> Depending on configuration of your machine - you may have to use `root` user for using
> `docker-compose`.

You can configure application by changing content of `backend/config.yml` file.

### API

If you've launched application with default config, you can:

> **NOTE**: `JOB_UUID` should be replaced with `job_id` received after registering a job.

- **register a job** with:

  > Params:
  >
  > **debug=1** (optional), will add to returned JSON field `next_url` which will allow you to
  > check status of assigned job

  ```bash
  curl -X PUT \
    'http://localhost:8191/api/jobs?debug=1' \
    -H 'Content-Type: application/json' \
    -d '{"url": "https://en.wikipedia.org/wiki/World_War_II"}'
  ```

  It will return something like below:

  ```json
  {
    "job_id": "JOB_UUID",
    "next_url": "http://localhost:8191/api/jobs/JOB_UUID/status?debug=1"
  }
  ```

- **check status of job** with:

  > Params:
  >
  > **debug=1** (optional), will add to returned JSON field `next_url` which will allow you to download
  > results of job

  ```bash
  curl -X GET \
    'http://localhost:8191/api/jobs/JOB_UUID/status'
  ```

  If job succeded, it will return something like below:

  ```json
  {
    "meta": {
      "imgs": {
        "done": 75,
        "failed": 0,
        "total": 75
      }
    },
    "status": "finished"
  }
  ```

- **download results of job as ZIP archive** with:

  > Params:
  >
  > **delete_after_download=1** (optional), after downloading ZIP archive, will delete job and
  > related data from database

  ```bash
  curl -X GET \
    'http://localhost:8191/api/jobs/JOB_UUID' \
    -O -J
  ```

## Running tests

```bash
docker-compose run --rm asyncpage /app/run_tests.sh
```

## Things to be done

- [ ] Tests for `Downloader`
- [ ] Tests for `Page`
- [ ] Simple demo for API

_By [Piotr Grędowski](mailto:piotrgredowski@gmail.com)_
