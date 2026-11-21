
from __future__ import annotations

import argparse
import json
import re
import socket
import sys
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import (
    HTTPRedirectHandler,
    Request,
    build_opener,
)


ROOT = Path(__file__).resolve().parents[1]

SOURCES = (
    ROOT / "README.md",
    ROOT / "docs" / "index.html",
    ROOT / "verification" / "references.md",
)

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.I)
URL_RE = re.compile(r"https?://[^\s<>\"'`]+", re.I)

ZENODO_DOI = "10.5281/zenodo.24245000"
ZENODO_URL = "https://zenodo.org/records/24245000"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
)


@dataclass
class CheckResult:
    target: str
    kind: str
    status: str
    http_status: int | None = None
    final_url: str | None = None
    reason: str | None = None
    required: bool = False


class LinkCheckerError(Exception):
    pass


class NoRedirectHandler(HTTPRedirectHandler):
    """Expose redirects so the checker can classify them."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class HTMLURLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: set[str] = set()

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                if value.startswith(("http://", "https://")):
                    self.urls.add(value)


def load_allowlist(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise LinkCheckerError(
            f"Cannot read allowlist {path}: {exc}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise LinkCheckerError(
            f"Invalid allowlist JSON: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise LinkCheckerError("Allowlist must be a JSON object.")

    for key in ("blocked_hosts", "blocked_dois"):
        if not isinstance(data.get(key, {}), dict):
            raise LinkCheckerError(
                f"Allowlist field '{key}' must be a JSON object."
            )

    return data


def extract_targets() -> tuple[set[str], set[str]]:
    urls: set[str] = set()
    dois: set[str] = set()

    for source in SOURCES:
        if not source.is_file():
            raise LinkCheckerError(
                f"Required source file is missing: {source}"
            )

        content = source.read_text(encoding="utf-8")

        if source.suffix.lower() == ".html":
            parser = HTMLURLParser()
            parser.feed(content)
            urls.update(parser.urls)
        else:
            for match in URL_RE.findall(content):
                urls.add(match.rstrip(".,;:!?)\"]}"))

        dois.update(
            doi.rstrip(".,;:!?)\"]}")
            for doi in DOI_RE.findall(content)
        )

    # DOI resolver links are checked separately as DOI targets.
    urls = {
        url for url in urls
        if urlparse(url).hostname != "doi.org"
    }

    urls.add(ZENODO_URL)
    dois.add(ZENODO_DOI)

    return urls, dois


def classify_status(
    status: int,
    headers,
) -> str:
    server = headers.get("Server", "").lower()
    cloudflare = (
        "cloudflare" in server
        or headers.get("CF-Ray") is not None
    )

    if status in (403, 429) or (status == 503 and cloudflare):
        return "blocked"

    if 300 <= status < 400:
        return "redirect"

    if 200 <= status < 300:
        return "OK"

    return "broken"


def is_allowlisted(
    target: str,
    kind: str,
    allowlist: dict,
) -> str | None:
    host = (urlparse(target).hostname or "").lower()

    blocked_hosts = allowlist.get("blocked_hosts", {})
    blocked_dois = allowlist.get("blocked_dois", {})

    if host in blocked_hosts:
        return str(blocked_hosts[host])

    if kind == "doi":
        doi = target.removeprefix("https://doi.org/")
        if doi in blocked_dois:
            return str(blocked_dois[doi])

    return None


def verify_zenodo_doi_with_datacite(
    timeout: float,
) -> tuple[bool, str]:
    """Independently verify the required Zenodo DOI through DataCite."""
    api_url = f"https://api.datacite.org/dois/{ZENODO_DOI}"
    request = Request(
        api_url,
        headers={"User-Agent": USER_AGENT},
    )

    try:
        opener = build_opener()
        response = opener.open(request, timeout=timeout)

        try:
            data = json.loads(response.read().decode("utf-8"))
        finally:
            response.close()

        attributes = data["data"]["attributes"]

        doi_matches = attributes.get("doi", "").lower() == ZENODO_DOI.lower()
        publisher_matches = (
            attributes.get("publisher", "").lower() == "zenodo"
        )
        registered_url = attributes.get("url", "")
        url_matches = (
            urlparse(registered_url).hostname == "zenodo.org"
            and urlparse(registered_url).path
            == f"/doi/{ZENODO_DOI}"
        )

        expected_identifier = f"oai:zenodo.org:24245000"
        identifiers = attributes.get("identifiers", [])
        record_matches = any(
            item.get("identifier") == expected_identifier
            and item.get("identifierType") == "oai"
            for item in identifiers
        )

        if all((
            doi_matches,
            publisher_matches,
            url_matches,
            record_matches,
        )):
            return True, (
                "DOI, Zenodo publisher, registered URL and record "
                "identifier independently verified through DataCite."
            )

        return False, (
            "DataCite metadata did not match all required Zenodo "
            "record details."
        )

    except (
        HTTPError,
        URLError,
        TimeoutError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
    ) as exc:
        return False, f"DataCite verification failed: {exc}"


def check_target(
    target: str,
    kind: str,
    timeout: float,
    allowlist: dict,
    required: bool = False,
) -> CheckResult:
    if not required:
        reason = is_allowlisted(target, kind, allowlist)
        if reason:
            return CheckResult(
                target=target,
                kind=kind,
                status="blocked",
                reason=f"Allowlisted: {reason}",
            )

    opener = build_opener(NoRedirectHandler())
    current_url = target
    redirected = False
    redirects = 0

    while True:
        request = Request(
            current_url,
            method="HEAD",
            headers={"User-Agent": USER_AGENT},
        )

        try:
            response = opener.open(request, timeout=timeout)
            status = response.status
            headers = response.headers
            final_url = response.geturl()
            response.close()

        except HTTPError as exc:
            status = exc.code
            headers = exc.headers
            final_url = current_url
            exc.close()

        except (URLError, TimeoutError, OSError) as exc:
            reason = getattr(exc, "reason", exc)

            if isinstance(reason, socket.gaierror):
                detail = "DNS lookup failed"
            elif isinstance(reason, (TimeoutError, socket.timeout)):
                detail = "Connection timed out"
            else:
                detail = str(reason)

            raise LinkCheckerError(
                f"Network unavailable or request failed for "
                f"{target}: {detail}"
            ) from exc

        classification = classify_status(status, headers)

        if classification == "redirect":
            location = headers.get("Location")

            if not location:
                return CheckResult(
                    target, kind, "redirect",
                    http_status=status,
                    final_url=final_url,
                    reason="Redirect response did not provide a Location header.",
                    required=required,
                )

            redirects += 1
            if redirects > 10:
                return CheckResult(
                    target, kind, "broken",
                    http_status=status,
                    final_url=current_url,
                    reason="Too many redirects.",
                    required=required,
                )

            redirected = True
            current_url = urljoin(current_url, location)
            continue

        if redirected and classification == "OK":
            if required:
                reason = "Resolved successfully through a redirect."
            else:
                return CheckResult(
                    target, kind, "redirect",
                    http_status=status,
                    final_url=current_url,
                    reason="Redirected to a responding destination.",
                )
        else:
            reason = None

        # Independently verify mandatory Zenodo targets when direct
        # automated access is blocked.
        required_zenodo_targets = {
            ZENODO_URL,
            f"https://doi.org/{ZENODO_DOI}",
        }

        if (
            required
            and target in required_zenodo_targets
            and classification == "blocked"
        ):
            verified, verification_reason = (
                verify_zenodo_doi_with_datacite(timeout)
            )

            if verified:
                classification = "OK"
                reason = (
                    f"Direct Zenodo access returned HTTP {status}; "
                    f"{verification_reason}"
                )
            else:
                reason = (
                    f"Direct Zenodo access returned HTTP {status}. "
                    f"{verification_reason}"
                )

        return CheckResult(
            target=target,
            kind=kind,
            status=classification,
            http_status=status,
            final_url=current_url,
            reason=reason,
            required=required,
        )


def write_reports(
    results: list[CheckResult],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    records = [asdict(result) for result in results]

    (output_dir / "link_report.json").write_text(
        json.dumps(records, indent=2),
        encoding="utf-8",
    )

    counts = {
        status: sum(
            result.status == status for result in results
        )
        for status in ("OK", "redirect", "blocked", "broken")
    }

    lines = [
        "# Link and DOI Check Report",
        "",
        f"- Total checked: {len(results)}",
        f"- OK: {counts['OK']}",
        f"- Redirect: {counts['redirect']}",
        f"- Blocked: {counts['blocked']}",
        f"- Broken: {counts['broken']}",
        "",
        "## Details",
        "",
    ]

    for result in results:
        detail = f" — {result.reason}" if result.reason else ""
        lines.append(
            f"- **{result.status.upper()}** — {result.target}{detail}"
        )

    (output_dir / "link_report.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Opt-in checker for repository links and DOIs."
    )

    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument(
        "--allowlist",
        type=Path,
        default=ROOT / "verification" / "link_allowlist.json",
    )
    parser.add_argument("--fail-on-broken", action="store_true")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "verification",
    )

    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    try:
        allowlist = load_allowlist(args.allowlist)
        urls, dois = extract_targets()

        # Check mandatory Zenodo targets first. If the network is
        # unavailable, stop with a clear error before checking everything.
        required_targets = [
            (ZENODO_URL, "url"),
            (f"https://doi.org/{ZENODO_DOI}", "doi"),
        ]

        results = []

        for target, kind in required_targets:
            results.append(
                check_target(
                    target,
                    kind,
                    args.timeout,
                    allowlist,
                    required=True,
                )
            )

        for url in sorted(urls - {ZENODO_URL}):
            results.append(
                check_target(url, "url", args.timeout, allowlist)
            )

        for doi in sorted(dois - {ZENODO_DOI}):
            results.append(
                check_target(
                    f"https://doi.org/{doi}",
                    "doi",
                    args.timeout,
                    allowlist,
                )
            )

        write_reports(results, args.output_dir)

    except (LinkCheckerError, OSError) as exc:
        print(f"Link checker error: {exc}", file=sys.stderr)
        return 2

    for result in results:
        print(f"{result.status.upper():8} {result.target}")

    required_failed = any(
        result.required and result.status != "OK"
        for result in results
    )

    broken_found = any(
        result.status == "broken" for result in results
    )

    if required_failed:
        print(
            "Required Zenodo DOI and record URL must both return OK.",
            file=sys.stderr,
        )
        return 1

    if args.fail_on_broken and broken_found:
        print("Broken links were found.", file=sys.stderr)
        return 1

    print(f"\nReports written to: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
