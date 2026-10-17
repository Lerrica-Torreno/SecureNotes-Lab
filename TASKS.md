# Combined Lab — Checklist

## Part A — make the security real (`app/main.py`)
- [x] **TASK 1 (A04)** hash_password / verify_password use bcrypt
- [x] **TASK 2 (A07)** create_token / read_token use a signed, expiring JWT
- [x] **TASK 3 (A07)** get_current_user raises 401 on a bad/expired token or unknown user (fail closed)
- [x] **TASK 4 (A01)** get_note returns 403 when the note isn't the caller's
- [x] **TASK 5 (A01)** /admin/users requires the admin role and never returns the password column

## Part B — write the tests (`tests/`)
API (`test_api.py`)
- [x] register then login returns a JWT (three dotted parts)
- [x] wrong password returns 401
- [x] create a note, then see it in your list
- [x] home endpoint returns the expected successful response

Security (`test_security.py`)
- [x] bad token rejected (401)
- [x] a user can't read another's note (403)  ← A01
- [x] a user can read their own note (200)
- [x] same login error for bad user vs bad password  ← A07
- [x] a non-admin can't list users (403)  ← A01
- [x] admin list has no password field  ← A04
- [x] missing authentication token rejected (401)

**Goal:** all 5 tasks done AND all 11 tests green (`pytest -q`). Then `pytest --cov=app`.

## Test Results

Command: python -m pytest -q

Result: 11 passed, 0 failed

Coverage command: python -m pytest --cov=app

Code coverage: 96%

Coverage details: 104 statements, 4 missed

Warnings: 6 non-blocking deprecation warnings from python-jose

The test suite verifies authentication, authorization, secure password handling, note ownership, and administrative access control.

## Reflection (4–5 sentences)
A key security test I implemented, test_user_cannot_read_another_users_note, verifies whether a user is blocked from accessing another user's private note. By confirming that the API returns HTTP 403 when Alice tries to access Bob's note, this test addresses OWASP A01: Broken Access Control. If a teammate were to accidentally remove the ownership check from get_note(), users might be able to access private information belonging to others. The automated test would catch this vulnerability by failing whenever the expected 403 response is not returned. This activity helped me grasp how security testing safeguards user data and keeps previously fixed vulnerabilities from being reintroduced.
