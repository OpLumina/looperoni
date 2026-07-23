#!/usr/bin/env python3
"""
looperoni.py - CLI Line Executor

Processes a text file line-by-line and executes a shell command for each line
with support for variable replacement and fixed or dynamic throttling.
"""

import argparse
import random
import subprocess
import sys
import time
from pathlib import Path


def parse_delay(delay_str: str) -> tuple[float, float] | float | None:
    """Parse the -d/--delay argument into a fixed float or a (min, max) tuple."""
    if not delay_str:
        return None

    try:
        if "," in delay_str:
            min_d, max_d = map(float, delay_str.split(",", 1))
            if min_d > max_d:
                raise ValueError("Min delay cannot be greater than max delay.")
            return (min_d, max_d)
        else:
            return float(delay_str)
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid delay format '{delay_str}': {e}")


def apply_throttle(delay: tuple[float, float] | float | None) -> None:
    """Sleep for the specified fixed or randomized delay duration."""
    if delay is None:
        return

    if isinstance(delay, tuple):
        min_d, max_d = delay
        sleep_time = random.uniform(min_d, max_d)
    else:
        sleep_time = delay

    time.sleep(sleep_time)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process a text file line-by-line and execute a shell command per line."
    )

    parser.add_argument(
        "-f", "--file",
        type=Path,
        required=True,
        help="Path to target text file."
    )
    parser.add_argument(
        "-e", "--exec",
        dest="exec_cmd",
        type=str,
        required=True,
        help="Shell command string to execute per line."
    )
    parser.add_argument(
        "-d", "--delay",
        type=parse_delay,
        default=None,
        help="Delay in seconds between executions: single float (e.g., '1.5') or range (e.g., '0.5,3.0')."
    )
    parser.add_argument(
        "-v", "--var",
        type=str,
        default="var",
        help="Variable placeholder name inside the exec command string. Default: 'var'."
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.file.is_file():
        print(f"Error: File '{args.file}' does not exist or is not a file.", file=sys.stderr)
        sys.exit(1)

    placeholder = f"{{{args.var}}}"

    try:
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            for line_num, line in enumerate(f, start=1):
                clean_line = line.rstrip("\r\n")
                cmd = args.exec_cmd.replace(placeholder, clean_line)
                try:
                    subprocess.run(cmd, shell=True, check=False)
                except KeyboardInterrupt:
                    print("\nExecution interrupted by user. Exiting.")
                    sys.exit(130)
                except Exception as e:
                    print(f"Error running command at line {line_num}: {e}", file=sys.stderr)
                apply_throttle(args.delay)

    except KeyboardInterrupt:
        print("\nProcess canceled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
