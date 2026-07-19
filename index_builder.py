"""
index_builder.py

Temporary placeholder.
"""

from pathlib import Path


def build_index(documents, output_folder: Path):
    index_file = output_folder / "INDEX.md"

    with open(index_file, "w", encoding="utf-8") as f:
        f.write("# EOS Document Index\n\n")

        for doc in documents:
            f.write(f"- {doc['filename']}\n")

    print(f"Created {index_file}")
