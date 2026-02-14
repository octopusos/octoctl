# Octoctl

Octoctl is the local control CLI for OctopusOS Manager.

It allows you to start, stop, inspect, and troubleshoot your local OctopusOS services from the terminal in a safe and auditable way.

## Installation

### macOS (Homebrew, recommended)

Install via Homebrew:

```bash
brew tap octopusos/octoctl
brew install octoctl
```

Verify installation:

```bash
octoctl --help
```

You should see the available commands: `status`, `start`, `stop`, `restart`, `logs`.

## Before You Use Octoctl

Octoctl communicates with a locally running OctopusOS Manager instance.

By default, it connects to:

`http://127.0.0.1:6110`

If the Manager is not running, Octoctl will not start it automatically. It will show a clear message explaining how to proceed.

## Starting The Manager

You have two supported ways to start OctopusOS Manager.

### Option A: From the system tray (recommended for desktop users)

1. Open the OctopusOS Tray application
1. Click Start Services

This launches the local Manager and all managed services.

### Option B: From the terminal

If you have the Manager installed locally:

```bash
octopus-manager
```

Or in development mode:

```bash
uv run octopus-manager
```

Once running, verify:

```bash
octoctl status
```

## Basic Usage

### Check system status

```bash
octoctl status
```

Returns the current state of:

- Manager
- Backend
- Frontend (if enabled)
- Mode (`PROBE` / `REAL`)
- Version and build metadata

### Start services

```bash
octoctl start
```

Starts all configured services under Manager control.

### Stop services

```bash
octoctl stop
```

Gracefully stops all managed services.

### Restart services

```bash
octoctl restart
```

Performs a controlled stop + start sequence.

### View logs

Tail recent logs:

```bash
octoctl logs --service backend --tail 200
```

Available services typically include: `manager`, `backend`, `frontend`.

## If The Manager Is Not Running

If you see an error like:

`Manager not reachable at http://127.0.0.1:6110`

It means:

- The Manager is not running
- Or it is running on a different port

What to do:

1. Start OctopusOS Manager (Tray or terminal)
1. Then retry:

```bash
octoctl status
```

## Advanced Configuration

### Custom Manager address

If your Manager runs on a different host or port:

```bash
OCTOCTL_BASE=http://127.0.0.1:7000 octoctl status
```

You may also export it:

```bash
export OCTOCTL_BASE=http://127.0.0.1:7000
```

## Design Principles

Octoctl is intentionally:

- Local-first
- Explicit (no silent auto-start behavior)
- Safe (no background mutations without Manager)
- Deterministic
- Compatible with `PROBE` and `REAL` modes

It does not bypass the Manager. All operations go through the local Control API.

## Troubleshooting

Check Manager health:

```bash
curl http://127.0.0.1:6110/control/health
```

Expected response:

```json
{
  "ok": true,
  "api_version": "v1",
  "mode": "PROBE",
  "octopusos_version": "...",
  "build": { "git_sha": "..." }
}
```

If this endpoint is not reachable, start the Manager first.

## Versioning

Each Octoctl release corresponds to a compatible Manager API version.

If a version mismatch occurs, Octoctl will report it explicitly.

## Security Notes

- Octoctl only connects to localhost by default.
- It does not expose remote control endpoints.
- All service lifecycle operations are mediated by the Manager.

## License

MIT License.

