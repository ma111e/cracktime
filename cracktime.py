import argparse
import re
import sys


def parse_human_speed(value):
    match = re.fullmatch(r"([\d.]+)\s*([kKmMgG]?)", value)
    if not match:
        raise argparse.ArgumentTypeError(f"Invalid speed format: {value}")
    number = float(match.group(1))
    suffix = match.group(2).lower()
    return number * {
        "": 1,
        "k": 1_000,
        "m": 1_000_000,
        "g": 1_000_000_000,
    }.get(suffix, 1)


def parse_length_range(value, exact_flag):
    """
    Behaviors:
      - "6-8" → range(6, 8)
      - "8" and exact=False → range(1, 8)
      - "8" and exact=True → range(8, 8)
    """
    if "-" in value:
        start, end = map(int, value.split("-"))
        if start > end or start < 1:
            raise argparse.ArgumentTypeError(f"Invalid length range: {value}")
        return range(start, end + 1)

    # Single number
    single = int(value)
    if single < 1:
        raise argparse.ArgumentTypeError("Length must be >= 1")

    if exact_flag:
        return range(single, single + 1)
    else:
        return range(1, single + 1)


def estimate_generation_time(length, charset_size, speed):
    combos = charset_size ** length
    return combos, combos / speed


def format_time(seconds):
    minute = 60
    hour = 3600
    day = 86400
    year = 31536000

    if seconds < minute:
        return f"{seconds:.2f} sec"
    if seconds < hour:
        return f"{seconds/minute:.2f} min"
    if seconds < day:
        return f"{seconds/hour:.2f} hr"
    if seconds < year:
        return f"{seconds/day:.2f} days"
    return f"{seconds/year:.2f} yrs"


def build_charset(args):
    charset = ""
    if args.lower:   charset += "abcdefghijklmnopqrstuvwxyz"
    if args.upper:   charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if args.digits:  charset += "0123456789"
    if args.symbols: charset += "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~"
    if args.custom:  charset += args.custom
    return charset


def print_ascii_table(data):
    headers = ["Length", "Keyspace", "Equation", "Total Combos", "Est. Time"]
    col_widths = [len(h) for h in headers]

    for row in data:
        for i, v in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(v)))

    print("+" + "+".join("-"*(w+2) for w in col_widths) + "+")
    print("| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |")
    print("+" + "+".join("="*(w+2) for w in col_widths) + "+")

    for row in data:
        print("| " + " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row))) + " |")

    print("+" + "+".join("-"*(w+2) for w in col_widths) + "+")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Brute-force keyspace time estimator")

    parser.add_argument("-l", "--length", required=True,
                        help="Length or range (8 → 1–8 unless --exact is used)")
    parser.add_argument("-s", "--speed", required=True, type=parse_human_speed)
    parser.add_argument("-k", "--keyspace", type=int,
                        help="Specify keyspace directly (overrides charset switches)")

    parser.add_argument("--exact", action="store_true", default=False,
                        help="Use only the provided length, do not expand from 1")

    parser.add_argument("-a", "--lower", action="store_true")
    parser.add_argument("-A", "--upper", action="store_true")
    parser.add_argument("-d", "--digits", action="store_true")
    parser.add_argument("-S", "--symbols", action="store_true")
    parser.add_argument("-c", "--custom", type=str)

    args = parser.parse_args()

    # Determine lengths (new logic)
    lengths = parse_length_range(args.length, args.exact)

    # Determine keyspace
    if args.keyspace:
        charset_size = args.keyspace
        print(f"[*] Using specified keyspace: {charset_size}")
    else:
        charset = build_charset(args)
        charset_size = len(charset)
        if charset_size == 0:
            print("Error: empty charset.")
            sys.exit(1)
        print(f"[*] Using composed charset ({charset_size} chars): {charset}")

    print(f"[*] Speed: {args.speed:.0f} per second\n")

    # Table
    rows = []
    for L in lengths:
        combos, secs = estimate_generation_time(L, charset_size, args.speed)
        eq = f"{charset_size}^{L} / {int(args.speed)}"
        rows.append([L, charset_size, eq, f"{combos:e}", format_time(secs)])

    print_ascii_table(rows)

    # Cumulative totals
    total_combos = sum(charset_size ** L for L in lengths)
    total_time = sum((charset_size ** L) / args.speed for L in lengths)

    print(f"[+] Total combinations: {total_combos:e}")
    print(f"[+] Total estimated time: {format_time(total_time)}")
