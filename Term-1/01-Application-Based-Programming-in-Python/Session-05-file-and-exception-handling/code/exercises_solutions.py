"""Session 05 practice solutions."""
import json
from pathlib import Path

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)


def file_stats(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return len(text.splitlines()), len(text.split()), len(text)


def ask_int(answers):
    """answers simulates successive input() calls."""
    for a in answers:
        try:
            return int(a)
        except ValueError:
            print(f"'{a}' is not a whole number, try again")
    return None


def filter_errors(src, dst):
    with open(src) as fin, open(dst, "w") as fout:
        for line in fin:
            if "error" in line.lower():
                fout.write(line)


def read_config(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


if __name__ == "__main__":
    sample = OUT / "sample.txt"
    sample.write_text("Python is fun\nFiles keep data\n", encoding="utf-8")
    print(file_stats(sample))
    assert file_stats(sample) == (2, 6, 30)
    assert ask_int(["ten", "4.5", "12"]) == 12
    log = OUT / "server.log"
    log.write_text("INFO start\nERROR disk full\nINFO ok\nerror timeout\n")
    filter_errors(log, OUT / "errors_only.log")
    print((OUT / "errors_only.log").read_text())
    assert read_config(OUT / "missing.json") == {}
