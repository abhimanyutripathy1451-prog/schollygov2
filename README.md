# SchollyGo v2 accounts

This is a standalone FastAPI and React account module. It uses only the `schollygoappv2` MySQL database. No legacy application imports are used.

## Setup

1. Create a MySQL user with access to a new `schollygoappv2` database. Copy `.env.example` to `.env`, set credentials and a random `OTP_SECRET` of at least 32 characters. Never reuse the legacy application's credentials in source control.
2. `python -m venv .venv` then `.venv\Scripts\python.exe -m pip install -r requirements.txt`
3. `.venv\Scripts\python.exe init_db.py` (set `SEED_DEV=true` to add the supplied CBSE curriculum choices).
4. `.venv\Scripts\python.exe -m uvicorn backend.main:app --port 8001`
5. In `frontend`: `npm install`, then `npm run dev`.

The initializer accepts only `schollygoappv2` or `schollygoappv2_test*` as database names, checks for unexpected tables, and uses idempotent additive SQL. The baseline is `sql/001_baseline.sql`. Back up and inspect an existing v2 database before running newer migrations. All application timestamps are UTC.

## OTP delivery

For local development, copy `.env.example` to `.env` and set real local database credentials and a random `OTP_SECRET`. The example explicitly enables `DEV_OTP_ENABLED=true`. The development OTP is `1234` for signup and recovery. For signup testing, an issued challenge accepts `1234` even after its normal expiry; it remains bound to the requested mobile and can be verified only once. The code is documented for local testing and is never returned by the API. Production startup rejects development mode. The SMS HTTP adapter needs `SMS_API_URL`, `SMS_API_KEY`, and `SMS_SENDER_ID`; its JSON shape must be adjusted to the selected provider before real delivery. No live delivery has been verified.

## API

OpenAPI: `http://127.0.0.1:8001/docs`. Endpoints: `GET /health`, `GET /curriculums`, `POST /auth/otp/request`, `POST /auth/otp/verify`, `POST /auth/signup`, `POST /auth/login`, `GET /auth/me`, `PATCH /auth/profile`, `POST /auth/reset-pin`, `POST /auth/logout`. Protected endpoints use `Authorization: Bearer <token>`. The OTP request returns a challenge ID; verify takes that ID, mobile, purpose and six digit code, then returns a one use grant. Signup and reset consume the grant.

## Tests

Use a separate disposable MySQL database named `schollygoappv2_test` and configure `DB_NAME=schollygoappv2_test`; never point test runs at the production database. Run `SEED_DEV=true python init_db.py`, then `PYTHONPATH=. DEV_OTP_ENABLED=true python tests/acceptance.py` and `python -m pytest tests/test_validation.py`. Browser checks: in `frontend`, run `npm run build` and `npm test`. The browser suite mocks the API; no automated test sends real SMS.

## Device sign-in

The v2 UI keeps its bearer session in localStorage until Log out, PIN reset, account disablement, or server-side revocation. New UI sign-ins request a persistent server session. Treat devices with an active session as trusted and use Log out on shared devices.





For local Windows development, run "powershell -ExecutionPolicy Bypass -File .\start.ps1" from the project root to start the backend and frontend together. Port 8001 is used because 8000 is unavailable on this machine.

## Dashboard UI

The authenticated home screen uses the v1 Basecamp dashboard visual layout. It displays the signed-in student and curriculum from the account API. Quest, learning metrics, Scorecard navigation, and subject cards are presentation placeholders until their modules are implemented; no learning API requests or fabricated progress values are used.

