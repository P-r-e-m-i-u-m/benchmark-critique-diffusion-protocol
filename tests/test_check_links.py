
from __future__ import annotations
import sys
import json
from urllib.error import URLError

import pytest

import check_links


def test_classify_http_status():
    assert check_links.classify_status(200, {}) == "OK"
    assert check_links.classify_status(301, {}) == "redirect"
    assert check_links.classify_status(403, {}) == "blocked"
    assert check_links.classify_status(429, {}) == "blocked"
    assert check_links.classify_status(404, {}) == "broken"


def test_cloudflare_response_is_blocked():
    headers = {"Server": "cloudflare"}
    assert check_links.classify_status(503, headers) == "blocked"


def test_allowlisted_host_is_blocked():
    allowlist = {
        "blocked_hosts": {
            "direct.mit.edu": "Known Cloudflare block"
        },
        "blocked_dois": {},
    }

    result = check_links.is_allowlisted(
        "https://direct.mit.edu/qss/article",
        "url",
        allowlist,
    )

    assert result == "Known Cloudflare block"


def test_allowlisted_doi_is_blocked():
    allowlist = {
        "blocked_hosts": {},
        "blocked_dois": {
            "10.1177/030631277800800305": "Known SAGE block"
        },
    }

    result = check_links.is_allowlisted(
        "https://doi.org/10.1177/030631277800800305",
        "doi",
        allowlist,
    )

    assert result == "Known SAGE block"


def test_required_target_bypasses_allowlist(monkeypatch):
    allowlist = {
        "blocked_hosts": {"zenodo.org": "Known block"},
        "blocked_dois": {
            check_links.ZENODO_DOI: "Known DOI block"
        },
    }

    class FakeResponse:
        status = 200
        headers = {}

        def geturl(self):
            return check_links.ZENODO_URL

        def close(self):
            pass

    class FakeOpener:
        def open(self, request, timeout):
            return FakeResponse()

    monkeypatch.setattr(
        check_links,
        "build_opener",
        lambda *args: FakeOpener(),
    )

    result = check_links.check_target(
        check_links.ZENODO_URL,
        "url",
        2,
        allowlist,
        required=True,
    )

    assert result.status == "OK"
    assert result.required is True


def test_network_failure_has_clear_error(monkeypatch):
    class FakeOpener:
        def open(self, request, timeout):
            raise URLError("Network is unavailable")

    monkeypatch.setattr(
        check_links,
        "build_opener",
        lambda *args: FakeOpener(),
    )

    with pytest.raises(
        check_links.LinkCheckerError,
        match="Network unavailable or request failed",
    ):
        check_links.check_target(
            "https://example.invalid",
            "url",
            2,
            {},
        )


def test_reports_are_written(tmp_path):
    results = [
        check_links.CheckResult(
            target="https://example.com",
            kind="url",
            status="OK",
            http_status=200,
        ),
        check_links.CheckResult(
            target="https://broken.example",
            kind="url",
            status="broken",
            http_status=404,
        ),
    ]

    check_links.write_reports(results, tmp_path)

    json_path = tmp_path / "link_report.json"
    markdown_path = tmp_path / "link_report.md"

    assert json_path.is_file()
    assert markdown_path.is_file()

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert len(data) == 2
    assert data[0]["status"] == "OK"
    assert "Broken: 1" in markdown_path.read_text(encoding="utf-8")



def test_datacite_verifies_zenodo_doi(monkeypatch):
    attributes = {
        "doi": check_links.ZENODO_DOI,
        "publisher": "Zenodo",
        "url": f"https://zenodo.org/doi/{check_links.ZENODO_DOI}",
        "identifiers": [
            {
                "identifier": "oai:zenodo.org:24245000",
                "identifierType": "oai",
            }
        ],
    }

    class FakeResponse:
        def read(self):
            return json.dumps({
                "data": {"attributes": attributes}
            }).encode("utf-8")

        def close(self):
            pass

    class FakeOpener:
        def open(self, request, timeout):
            assert request.full_url == (
                f"https://api.datacite.org/dois/{check_links.ZENODO_DOI}"
            )
            return FakeResponse()

    monkeypatch.setattr(
        check_links,
        "build_opener",
        lambda *args: FakeOpener(),
    )

    verified, reason = (
        check_links.verify_zenodo_doi_with_datacite(5)
    )

    assert verified is True
    assert "independently verified" in reason


def test_datacite_rejects_mismatched_zenodo_record(monkeypatch):
    attributes = {
        "doi": check_links.ZENODO_DOI,
        "publisher": "Other publisher",
        "url": "https://example.com/incorrect-record",
        "identifiers": [],
    }

    class FakeResponse:
        def read(self):
            return json.dumps({
                "data": {"attributes": attributes}
            }).encode("utf-8")

        def close(self):
            pass

    class FakeOpener:
        def open(self, request, timeout):
            return FakeResponse()

    monkeypatch.setattr(
        check_links,
        "build_opener",
        lambda *args: FakeOpener(),
    )

    verified, reason = (
        check_links.verify_zenodo_doi_with_datacite(5)
    )

    assert verified is False
    assert "did not match" in reason



def test_required_zenodo_check_uses_datacite_after_403(monkeypatch):
    from email.message import Message
    from urllib.error import HTTPError

    attributes = {
        "doi": check_links.ZENODO_DOI,
        "publisher": "Zenodo",
        "url": f"https://zenodo.org/doi/{check_links.ZENODO_DOI}",
        "identifiers": [
            {
                "identifier": "oai:zenodo.org:24245000",
                "identifierType": "oai",
            }
        ],
    }

    class FakeResponse:
        status = 200
        headers = {}

        def read(self):
            return json.dumps({
                "data": {"attributes": attributes}
            }).encode("utf-8")

        def geturl(self):
            return "https://api.datacite.org/"

        def close(self):
            pass

    class FakeOpener:
        def open(self, request, timeout):
            if request.full_url == check_links.ZENODO_URL:
                raise HTTPError(
                    request.full_url,
                    403,
                    "Forbidden",
                    Message(),
                    None,
                )

            return FakeResponse()

    monkeypatch.setattr(
        check_links,
        "build_opener",
        lambda *args: FakeOpener(),
    )

    result = check_links.check_target(
        check_links.ZENODO_URL,
        "url",
        5,
        {},
        required=True,
    )

    assert result.status == "OK"
    assert result.http_status == 403
    assert result.required is True
    assert "independently verified" in result.reason


def test_cli_network_failure_shows_clear_error(monkeypatch, capsys):
    class FakeOpener:
        def open(self, request, timeout):
            raise URLError("Network is unavailable")

    monkeypatch.setattr(
        check_links,
        "build_opener",
        lambda *args: FakeOpener(),
    )

    monkeypatch.setattr(
        sys,
        "argv",
        ["check_links.py"],
    )

    exit_code = check_links.main()
    captured = capsys.readouterr()

    assert exit_code != 0
    assert "Link checker error:" in captured.err
    assert "Traceback" not in captured.err
    assert "Traceback" not in captured.out

def test_fail_on_broken_returns_nonzero(monkeypatch, tmp_path):
    from email.message import Message
    from urllib.error import HTTPError

    class FakeResponse:
        def __init__(self, url):
            self.url = url
            self.status = 200
            self.headers = {}

        def geturl(self):
            return self.url

        def close(self):
            pass

    class FakeOpener:
        def open(self, request, timeout):
            if request.full_url == "https://broken.example/test":
                raise HTTPError(
                    request.full_url,
                    404,
                    "Not Found",
                    Message(),
                    None,
                )

            return FakeResponse(request.full_url)

    monkeypatch.setattr(
        check_links,
        "build_opener",
        lambda *args: FakeOpener(),
    )

    monkeypatch.setattr(
        check_links,
        "extract_targets",
        lambda: ({"https://broken.example/test"}, set()),
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "check_links.py",
            "--fail-on-broken",
            "--output-dir",
            str(tmp_path),
        ],
    )

    exit_code = check_links.main()

    assert exit_code != 0

    data = json.loads(
        (tmp_path / "link_report.json").read_text(encoding="utf-8")
    )

    broken = [
        item for item in data
        if item["target"] == "https://broken.example/test"
    ]

    assert len(broken) == 1
    assert broken[0]["status"] == "broken"

def test_extract_targets_strips_trailing_doi_punctuation(tmp_path, monkeypatch):
    source = tmp_path / "references.md"
    source.write_text(
        "Reference DOI: 10.1234/example.\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(check_links, "SOURCES", (source,))
    urls, dois = check_links.extract_targets()

    assert "10.1234/example" in dois
    assert "10.1234/example." not in dois