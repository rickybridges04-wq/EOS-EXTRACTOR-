"""
markdown_detector.py

Advanced Markdown document detector for ChatGPT exports.
Version 2
"""

import re

# Matches filenames like:
# 001_DOCUMENT.md
# ENTERPRISE_STANDARD.md
# My File.md
FILENAME_PATTERN = re.compile(
    r'([A-Za-z0-9 _\-.]+\.md)',
    re.IGNORECASE
)

# Matches Markdown headings
HEADING_PATTERN = re.compile(
    r'^\s*#{1,6}\s+.+',
    re.MULTILINE
)

# Matches fenced Markdown/code blocks
CODEBLOCK_PATTERN = re.compile(
    r"```(?:markdown|md)?\n(.*?)```",
    re.DOTALL | re.IGNORECASE
)


def extract_text(node):
    """
    Safely extract text from a ChatGPT message node.
    """

    try:
        message = node.get("message")

        if not message:
            return ""

        content = message.get("content")

        if not content:
            return ""

        if content.get("content_type") != "text":
            return ""

        return "\n".join(content.get("parts", []))

    except Exception:
        return ""


def guess_filename(text, counter):

    match = FILENAME_PATTERN.search(text)

    if match:
        return match.group(1).strip()

    heading = HEADING_PATTERN.search(text)

    if heading:

        title = heading.group()

        title = title.lstrip("#").strip()

        title = re.sub(r"[<>:\"/\\\\|?*]", "_", title)

        title = title.replace(" ", "_")

        return f"{counter:03d}_{title}.md"

    return f"{counter:03d}_Recovered_Document.md"


def find_markdown_documents(conversations):

    documents = []

    seen = set()

    counter = 1

    for conversation in conversations:

        mapping = conversation.get("mapping", {})

        for node in mapping.values():

            text = extract_text(node)

            if not text.strip():
                continue

            filename = guess_filename(text, counter)

            content = text

            blocks = CODEBLOCK_PATTERN.findall(text)

            if blocks:
                content = max(blocks, key=len)

            key = (filename, content[:300])

            if key in seen:
                continue

            seen.add(key)

            documents.append(
                {
                    "filename": filename,
                    "content": content,
                    "conversation": conversation.get("title", "Unknown")
                }
            )

            counter += 1

    return documents
