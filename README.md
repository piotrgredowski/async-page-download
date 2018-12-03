[![Build Status](https://travis-ci.com/piotrgredowski/async-page-download.svg?branch=master)](https://travis-ci.com/piotrgredowski/async-page-download)
[![codecov](https://codecov.io/gh/piotrgredowski/async-page-download/branch/develop/graph/badge.svg)](https://codecov.io/gh/piotrgredowski/async-page-download)

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

- [Register a job](./api_docs/register_job.md)
- [Check status of the job](./api_docs/check_status_of_job.md)
- [Get result of the job](./api_docs/get_result_of_job.md)

## Running tests

```bash
docker-compose run --rm asyncpage /app/run_tests.sh
```

## Things to be done

- [ ] Tests for `Downloader`
- [ ] Tests for `Page`
- [ ] Simple demo for API

_By [Piotr Grędowski](mailto:piotrgredowski@gmail.com)_
