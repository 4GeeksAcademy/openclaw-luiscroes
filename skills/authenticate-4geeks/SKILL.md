---
name: authenticate-4geeks
description: Verify the 4Geeks student API session by calling only GET /v1/admissions/user/me and report its status without exposing credentials or personal identifiers.
---

# Authenticate 4Geeks

1. Run the bundled helper `scripts/check_session.py` with Python 3; it is the only permitted API caller for this skill and requests only the documented self-profile endpoint.
2. Read its single-line sanitized result. On HTTP 200, report `sesión activa` with the returned username/name if present, otherwise `sesión activa` without a name. On HTTP 401 or 403, report `token rechazado; puede haber caducado y hay que renovarlo`. For missing credentials, network errors, or other status codes, report only a short generic diagnostic; never characterize them as an expired token.
3. Never display or log the token, Authorization header, email, IDs, or raw response body. Do not make any other request or perform any write action.
4. Verify the helper is executable through Python and returns only a sanitized status/name; do not expose diagnostic details that can contain sensitive data.
