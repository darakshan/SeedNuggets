# Seed Nuggets — build
# Requires: python3, just  (brew install just)
# Run `just setup` once to create .venv and install dependencies.

root := justfile_directory()
python := root + "/.venv/bin/python"

# Create venv and install dependencies (run once)
setup:
    python3 -m venv {{root}}/.venv
    {{root}}/.venv/bin/pip install -r {{root}}/requirements.txt

# Rebuild the full site from nuggets/
build:
    {{python}} {{root}}/src/build.py

# Rebuild a single nugget (e.g. just build-nugget 001)
build-nugget nugget:
    {{python}} {{root}}/src/build.py --nugget {{nugget}}
