#!/usr/bin/env python3
"""Build a cron expression from simple inputs."""
import argparse
import sys

PRESETS = {
    "every-minute": "* * * * *",
    "hourly": "0 * * * *",
    "daily": "0 0 * * *",
    "weekly": "0 0 * * 0",
    "monthly": "0 0 1 * *",
    "yearly": "0 0 1 1 *",
    "weekdays": "0 9 * * 1-5",
    "weekends": "0 9 * * 6,0",
}

DAYS = {"sun": 0, "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6}


def parse_days(value):
    """Accept 0-6, names (mon, tue...), ranges (mon-fri) or comma lists."""
    out = []
    for part in value.split(","):
        part = part.strip().lower()
        if "-" in part:
            a, b = part.split("-", 1)
            a = DAYS.get(a, a)
            b = DAYS.get(b, b)
            try:
                lo, hi = int(a), int(b)
            except ValueError:
                raise ValueError(f"bad day range: {part}")
            if not (0 <= lo <= 6 and 0 <= hi <= 6 and lo <= hi):
                raise ValueError(f"bad day range: {part}")
            out.extend(range(lo, hi + 1))
        else:
            v = DAYS.get(part, part)
            try:
                n = int(v)
            except ValueError:
                raise ValueError(f"bad day of week: {part}")
            if not 0 <= n <= 6:
                raise ValueError(f"day of week must be 0-6: {part}")
            out.append(n)
    return ",".join(str(n) for n in sorted(set(out)))


def describe(expr, command):
    minute, hour, dom, month, dow = expr.split()
    parts = [f"Cron expression: {expr}"]
    if command:
        parts.append(f"Command:         {command}")
        parts.append(f"Full crontab line: {expr} {command}")
    if minute.startswith("*/"):
        parts.append(f"Runs every {minute[2:]} minute(s).")
    elif hour == "*" and minute != "*":
        parts.append(f"Runs at minute {minute} of every hour.")
    elif dom == "*" and month == "*" and dow == "*":
        parts.append(f"Runs daily at {hour}:{minute.zfill(2)}.")
    else:
        parts.append(f"Runs at {hour}:{minute.zfill(2)} "
                     f"(day {dom}, month {month}, weekday {dow}).")
    return "\n".join(parts)


def main():
    p = argparse.ArgumentParser(description="Build a cron expression from simple inputs.")
    p.add_argument("--preset", choices=sorted(PRESETS),
                   help="Use a preset schedule instead of custom options")
    p.add_argument("--minute", default="0", help="Minute 0-59 or */N (default: 0)")
    p.add_argument("--hour", default="0", help="Hour 0-23 or */N (default: 0)")
    p.add_argument("--day", default="*", help="Day of month 1-31 (default: *)")
    p.add_argument("--month", default="*", help="Month 1-12 (default: *)")
    p.add_argument("--weekday", default="*",
                   help="Day of week 0-6, name (mon), range (mon-fri) or list (default: *)")
    p.add_argument("--every", type=int, help="Every N minutes (shorthand for --minute '*/N' --hour '*')")
    p.add_argument("--command", help="Command to schedule; prints a full crontab line")
    p.add_argument("--list-presets", action="store_true", help="List available presets and exit")
    args = p.parse_args()

    if args.list_presets:
        for name in sorted(PRESETS):
            print(f"{name:<14} {PRESETS[name]}")
        return 0

    if args.preset:
        expr = PRESETS[args.preset]
    else:
        minute, hour = args.minute, args.hour
        if args.every is not None:
            if args.every < 1 or args.every > 59:
                p.error("--every must be between 1 and 59")
            minute, hour = f"*/{args.every}", "*"
        try:
            weekday = parse_days(args.weekday) if args.weekday != "*" else "*"
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        expr = f"{minute} {hour} {args.day} {args.month} {weekday}"

    print(describe(expr, args.command))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
