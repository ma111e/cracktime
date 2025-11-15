# Cracktime

NAME
       cracktime.py – estimate brute-force keyspace generation time

SYNOPSIS
       python cracktime.py [OPTIONS]

DESCRIPTION
       cracktime.py computes the total number of possible combinations for a
       given keyspace and one or more string lengths, then estimates the time
       required to enumerate those combinations at a specified generation
       speed. Output is presented in an ASCII table, followed by cumulative
       totals for all evaluated lengths.

LENGTH BEHAVIOR
       If a single length L is provided (e.g., -l 8), cracktime.py defaults
       to calculating all lengths from 1 through L.

       To restrict calculations strictly to L, use the --exact option.

OPTIONS
       -l, --length LENGTH
              Specify string length or length range.
              Examples:
                 8          → lengths 1 through 8
                 8 --exact  → length 8 only
                 3-8        → lengths 3 through 8

       -s, --speed SPEED
              Specify generation speed in human-readable units.
              Supports suffixes: k, M, G.
              Examples: 50M, 500k, 2.5G.

       -k, --keyspace SIZE
              Specify total keyspace size directly. Overrides charset switches.

       --exact
              Use only the provided length, even when a single number is given.

CHARSET OPTIONS
       -a, --lower
              Include lowercase letters a–z.

       -A, --upper
              Include uppercase letters A–Z.

       -d, --digits
              Include digits 0–9.

       -S, --symbols
              Include common symbols.

       -c, --custom CHARACTERS
              Include custom characters in the charset.

NOTES
       When --keyspace is provided, charset switches (-a, -A, -d, -S, -c) are ignored.

       If neither --keyspace nor any charset components are specified,
       cracktime.py exits with an error.

OUTPUT
       cracktime.py produces an ASCII table with the following columns:

              Length       the evaluated string length
              Keyspace     number of possible characters
              Equation     formula used in calculation
              Total Combos total number of combinations
              Est. Time    estimated enumeration time

       After the table, cumulative totals across all evaluated lengths are printed,
       including total combinations and total estimated time.

EXAMPLES
       Using a composed charset:
              python cracktime.py -l 6-8 -s 50M -a -A -d

       Using a direct keyspace:
              python cracktime.py -l 8 -s 100M -k 62

       Restricting to a single exact length:
              python cracktime.py -l 8 -s 50M --exact

EXIT STATUS
       0      Successful execution
       1      Invalid arguments or empty charset

AUTHOR
       Developed as a simple educational utility for estimating brute-force
       enumeration times. cracktime.py performs no brute-forcing.

LICENSE
       MIT

