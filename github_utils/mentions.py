import os
import re

ATLAS_MENTION = "atlas-world-ai"
CODERABBIT_MENTION = os.getenv("CODERABBIT_MENTION", "coderabbitai")

ATLAS_MENTION_PATTERN = re.compile(
    rf"@(?:\[{ATLAS_MENTION}\]\([^)]+\)|{ATLAS_MENTION})\b",
    re.IGNORECASE,
)


def contains_atlas_mention(body: str) -> bool:
    return bool(ATLAS_MENTION_PATTERN.search(body))


def to_coderabbit_comment(body: str) -> str:
    converted = ATLAS_MENTION_PATTERN.sub(f"@{CODERABBIT_MENTION}", body).strip()
    remainder = converted.split(f"@{CODERABBIT_MENTION}", 1)[-1].strip()
    if not remainder:
        return f"@{CODERABBIT_MENTION} review"
    return converted
