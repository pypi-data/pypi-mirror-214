import argparse
import concurrent.futures
import json
from pathlib import Path
from threading import Event

from sword_to_json.books_from_sword import generate_books
from sword_to_json.utils import metadata
from sword_to_json.utils.progress import Progress


def main():
    parser = argparse.ArgumentParser(description=metadata.summary)
    parser.add_argument("sword", help="path to zipped sword module")
    parser.add_argument("module", help="name of the sword module to load")
    parser.add_argument("-o", "--output", help="path to write generated JSON file")
    parser.add_argument("-v", "--version", action="version", version=f"{metadata.name} {metadata.version}")

    args = parser.parse_args()

    if args.output is None:
        args.output = f"{Path(args.sword).resolve().parent}/{args.module}.json"

    with open(args.output, "w") as outfile:
        books = generate_books(args.sword, args.module)
        progress = Progress(title=f"Saving to {outfile.name}")
        event = Event()
        executor = concurrent.futures.ThreadPoolExecutor()
        executor.submit(progress.infinite, event)
        json.dump({"books": books}, outfile)
        event.set()


if __name__ == "__main__":
    main()
