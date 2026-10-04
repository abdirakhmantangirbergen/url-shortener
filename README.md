# URL Shortener Service

A minimal and fast URL Shortener HTTP service built with Python and FastAPI.

## Features

- `GET /` — Service status / greeting.
- `GET /healthz` — Lightweight health check endpoint (returns 200 without external dependencies).
- `POST /shorten` — Shortens a given URL and returns a unique short identifier.
- `GET /{short_id}` — Redirects to the original URL.

## Configuration & Port

The service listens on the port specified by the `PORT` environment variable.
If `PORT` is not defined, it defaults to port `8080`.

Example:
```bash
export PORT=9000
./scripts/run.sh
```

## Running the Service

Start the service using the run script:

```bash
./scripts/run.sh
```

The script will automatically set up the virtual environment, install dependencies, and launch the server.

## Running Tests

Run the test suite using the test script:

```bash
./scripts/test.sh
```

The test runner will execute all unit and integration tests and output test summary in standard format: `TESTS: 4/4`.
