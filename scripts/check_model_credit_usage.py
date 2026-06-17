#!/usr/bin/env python3
"""Check model credit / usage without exposing secrets.

This script is designed for the public my-sprees-docs repo, but reads all
credentials from environment variables at runtime. It prints a safe summary and
never prints API keys or bearer tokens.

Supported live API checks:
- OpenRouter: OPENROUTER_API_KEY -> /api/v1/credits
- DeepSeek: DEEPSEEK_API_KEY -> /user/balance
- OpenAI Admin/API key: OPENAI_ADMIN_KEY or OPENAI_API_KEY -> organization costs
- Local Hermes usage: `hermes insights --days N` if the Hermes CLI is installed

Providers that only expose quota in a web console or OAuth subscription layer are
reported as MANUAL so the dashboard does not pretend to know unavailable data.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class CheckResult:
    provider: str
    status: str
    credit_remaining: str = "—"
    usage: str = "—"
    source: str = "—"
    note: str = ""


def request_json(url: str, token: str, *, timeout: int = 20) -> tuple[int, dict[str, Any] | list[Any] | None, str | None]:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "my-sprees-docs-credit-usage-check/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            return response.status, json.loads(raw), None
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")[:500]
        return exc.code, None, raw or str(exc)
    except Exception as exc:  # noqa: BLE001 - CLI should capture all provider failures
        return 0, None, str(exc)


def fmt_money(value: Any) -> str:
    try:
        return f"${float(value):,.4f}"
    except Exception:
        return str(value) if value is not None else "—"


def check_openrouter() -> CheckResult:
    token = os.getenv("OPENROUTER_API_KEY")
    if not token:
        return CheckResult("OpenRouter", "MISSING_KEY", source="OPENROUTER_API_KEY", note="set env var to enable live credit check")
    code, data, error = request_json("https://openrouter.ai/api/v1/credits", token)
    if code == 200 and isinstance(data, dict):
        payload = data.get("data", data)
        credits = payload.get("total_credits")
        usage = payload.get("total_usage")
        remaining = None
        if credits is not None and usage is not None:
            try:
                remaining = float(credits) - float(usage)
            except Exception:
                remaining = None
        return CheckResult(
            "OpenRouter",
            "OK",
            credit_remaining=fmt_money(remaining) if remaining is not None else "—",
            usage=fmt_money(usage),
            source="/api/v1/credits",
            note=f"total credits {fmt_money(credits)}",
        )
    return CheckResult("OpenRouter", "FAIL", source="/api/v1/credits", note=f"HTTP {code}: {error or 'unexpected response'}")


def check_deepseek() -> CheckResult:
    token = os.getenv("DEEPSEEK_API_KEY")
    if not token:
        return CheckResult("DeepSeek", "MISSING_KEY", source="DEEPSEEK_API_KEY", note="set env var to enable live balance check")
    code, data, error = request_json("https://api.deepseek.com/user/balance", token)
    if code == 200 and isinstance(data, dict):
        infos = data.get("balance_infos") or []
        parts = []
        total = 0.0
        for item in infos:
            currency = item.get("currency", "")
            balance = item.get("total_balance") or item.get("granted_balance") or item.get("topped_up_balance")
            if balance is not None:
                parts.append(f"{balance} {currency}".strip())
                try:
                    total += float(balance)
                except Exception:
                    pass
        return CheckResult(
            "DeepSeek",
            "OK" if data.get("is_available", True) else "WARN",
            credit_remaining=", ".join(parts) or "—",
            source="/user/balance",
            note="account available" if data.get("is_available", True) else "account not available",
        )
    return CheckResult("DeepSeek", "FAIL", source="/user/balance", note=f"HTTP {code}: {error or 'unexpected response'}")


def check_openai(days: int) -> CheckResult:
    token = os.getenv("OPENAI_ADMIN_KEY") or os.getenv("OPENAI_API_KEY")
    if not token:
        return CheckResult("OpenAI API", "MISSING_KEY", source="OPENAI_ADMIN_KEY / OPENAI_API_KEY", note="Codex/OAuth subscription access may not expose billing API")
    start_time = int(time.time()) - days * 86400
    query = urllib.parse.urlencode({"start_time": start_time, "limit": min(max(days, 1), 180)})
    url = f"https://api.openai.com/v1/organization/costs?{query}"
    code, data, error = request_json(url, token)
    if code == 200 and isinstance(data, dict):
        total = 0.0
        for bucket in data.get("data", []):
            for result in bucket.get("results", []):
                amount = ((result.get("amount") or {}).get("value"))
                if amount is not None:
                    try:
                        total += float(amount)
                    except Exception:
                        pass
        return CheckResult("OpenAI API", "OK", usage=fmt_money(total), source="/v1/organization/costs", note=f"last {days} days; requires eligible admin/API key")
    return CheckResult("OpenAI API", "WARN", source="/v1/organization/costs", note=f"HTTP {code}: {error or 'cost endpoint unavailable for this credential'}")


def check_hermes_insights(days: int) -> CheckResult:
    if not shutil.which("hermes"):
        return CheckResult("Hermes local usage", "MISSING_TOOL", source="hermes insights", note="Hermes CLI not on PATH")
    try:
        proc = subprocess.run(
            ["hermes", "insights", "--days", str(days)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
            check=False,
        )
    except Exception as exc:  # noqa: BLE001
        return CheckResult("Hermes local usage", "FAIL", source="hermes insights", note=str(exc))
    compact = " ".join(proc.stdout.split())[:220]
    return CheckResult(
        "Hermes local usage",
        "OK" if proc.returncode == 0 else "WARN",
        usage=f"see hermes insights --days {days}",
        source="local session DB",
        note=compact or f"exit code {proc.returncode}",
    )


def manual_provider(name: str, note: str) -> CheckResult:
    return CheckResult(name, "MANUAL", source="provider console / OAuth subscription", note=note)


def collect(days: int) -> list[CheckResult]:
    return [
        check_hermes_insights(days),
        check_openrouter(),
        check_openai(days),
        check_deepseek(),
        manual_provider("Anthropic", "usage/cost visibility depends on Admin API or provider console access"),
        manual_provider("Gemini / Google", "credit is normally in Google Cloud Billing; API-key quota is in Google AI Studio / Cloud Console"),
        manual_provider("xAI / Grok", "check provider console unless an account-level billing API is configured"),
        manual_provider("MiniMax OAuth", "current subscription/OAuth path is usable for model calls but no public credit endpoint is configured here"),
    ]


def print_markdown(results: list[CheckResult], days: int) -> None:
    now = dt.datetime.now(dt.timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")
    print(f"# Model Credit & Usage Check\n")
    print(f"Generated: {now}; window: last {days} days\n")
    print("| Provider | Status | Credit remaining | Usage | Source | Note |")
    print("|---|---|---:|---:|---|---|")
    for r in results:
        note = r.note.replace("|", "\\|")
        print(f"| {r.provider} | {r.status} | {r.credit_remaining} | {r.usage} | `{r.source}` | {note} |")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check model provider credit and usage safely from env vars.")
    parser.add_argument("--days", type=int, default=30, help="usage window for providers that support date ranges")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    results = collect(args.days)
    if args.format == "json":
        print(json.dumps([asdict(r) for r in results], ensure_ascii=False, indent=2))
    else:
        print_markdown(results, args.days)
    return 0


if __name__ == "__main__":
    sys.exit(main())
