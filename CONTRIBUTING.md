# Contributing

Thanks for helping improve VOIDSCAN. Keep changes focused, readable, typed, and
compatible with Linux systems where optional hardware and sensor details may be
unavailable.

1. Fork the repository and create a focused branch.
2. Create a virtual environment and install the project with `pip install -e '.[dev]'`.
3. Run `python -m unittest discover -s tests` and check every changed CLI path.
4. Open a pull request with a clear summary and testing notes.

Please do not add collection of secrets or public IP lookups, privileged
operations, automatic package installation, or system/network changes.
