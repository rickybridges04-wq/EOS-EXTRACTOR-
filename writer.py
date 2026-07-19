"""
writer.py

Writes recovered Markdown documents to disk.
"""

from pathlib import Path
import re


def sanitize_filename(filename: str) -> str:
    """
    Remove characters that are invalid in filenames.
    """

    filename = re.sub(r'[<>:"/\\\\|?*]', "_", filename)
    filename = filename.strip()

    if not filename.lower().endswith(".md"):
        filename += ".md"

    return filename


def write_documents(documents, output_folder: Path):

    markdown_folder = output_folder / "markdown"

    markdown_folder.mkdir(parents=True, exist_ok=True)

    written = 0

    for document in documents:

        filename = sanitize_filename(document["filename"])

        output_file = markdown_folder / filename

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(document["content"])

        written += 1

    print()
    print("=" * 60)
    print("Markdown Export")
    print("=" * 60)
    print(f"Wrote {written} Markdown documents.")
    print(f"Location: {markdown_folder}")
    print()
