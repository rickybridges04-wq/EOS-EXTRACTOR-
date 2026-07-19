"""
markdown_detector.py

Scans ChatGPT conversations for Markdown documents.
"""

import re


FILENAME_PATTERN = re.compile(
    r'([A-Za-z0-9_\- ]+\.md)',
    re.IGNORECASE
)


def extract_text(node):
    """
    Safely extracts text from a ChatGPT message node.
    """

    try:
        content = node["message"]["content"]

        if content["content_type"] == "text":
            return "\n".join(content["parts"])

    except Exception:
        return ""

    return ""


def find_markdown_documents(conversations):

    documents = []

    for conversation in conversations:

        mapping = conversation.get("mapping", {})

        for node in mapping.values():

            text = extract_text(node)

            if not text:
                continue

            filename_match = FILENAME_PATTERN.search(text)

            if filename_match:

                filename = filename_match.group(1)

                documents.append(
                    {
                        "filename": filename,
                        "content": text,
                        "conversation": conversation.get("title", "Unknown")
                    }
                )

    return documents
