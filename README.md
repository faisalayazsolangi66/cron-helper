# Cron Helper

Build a cron expression from simple inputs, or pick a preset schedule.

## Requirements

- Python 3.8+
- Standard library only — no third-party packages

## Usage

```bash
python3 main.py --list-presets
python3 main.py --preset daily --command "/usr/bin/python3 /home/user/backup.py"
python3 main.py --hour 9 --minute 30 --weekday mon-fri --command "/usr/bin/backup.sh"
python3 main.py --every 15
```

## Example

```bash
$ python3 main.py --preset weekdays --command "/usr/bin/backup.sh"
Cron expression: 0 9 * * 1-5
Command:         /usr/bin/backup.sh
Full crontab line: 0 9 * * 1-5 /usr/bin/backup.sh
Runs at 0:09 (day *, month *, weekday 1-5).
```

## License

MIT — see [LICENSE](LICENSE).
