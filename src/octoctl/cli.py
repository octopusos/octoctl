from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_BASE = os.environ.get("OCTOCTL_BASE", "http://127.0.0.1:6110").rstrip("/")


def _request(method: str, path: str, *, timeout: float = 5.0) -> dict:
    url = DEFAULT_BASE + path
    req = urllib.request.Request(url, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        raise RuntimeError(f"HTTP {e.code} from manager: {body or e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(
            "\n".join(
                [
                    f"Manager not reachable at {DEFAULT_BASE}.",
                    "Start it first (e.g. `octopus-manager`) or open Tray -> Start.",
                    f"Underlying error: {e}",
                ]
            )
        ) from e


def cmd_status(_args: argparse.Namespace) -> int:
    payload = _request("GET", "/control/status")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_start(_args: argparse.Namespace) -> int:
    payload = _request("POST", "/control/start")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_stop(_args: argparse.Namespace) -> int:
    payload = _request("POST", "/control/stop")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_restart(_args: argparse.Namespace) -> int:
    payload = _request("POST", "/control/restart")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_logs(args: argparse.Namespace) -> int:
    params = urllib.parse.urlencode({"service": args.service, "tail": str(args.tail)})
    payload = _request("GET", f"/control/logs?{params}")
    if isinstance(payload, dict) and isinstance(payload.get("lines"), list):
        for line in payload["lines"]:
            print(line)
        return 0
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="octoctl", description="OctopusOS local manager control CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status").set_defaults(fn=cmd_status)
    sub.add_parser("start").set_defaults(fn=cmd_start)
    sub.add_parser("stop").set_defaults(fn=cmd_stop)
    sub.add_parser("restart").set_defaults(fn=cmd_restart)

    lp = sub.add_parser("logs")
    lp.add_argument("--service", default="backend", help="backend|frontend|manager")
    lp.add_argument("--tail", type=int, default=200)
    lp.set_defaults(fn=cmd_logs)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    try:
        args = build_parser().parse_args(argv)
        return int(args.fn(args))
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
