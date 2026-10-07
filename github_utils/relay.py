from github_utils.client import post_pr_comment
from github_utils.mentions import (
    ATLAS_MENTION,
    CODERABBIT_MENTION,
    contains_atlas_mention,
    to_coderabbit_comment,
)


async def relay_mention(payload: dict, pr_number: int) -> dict:
    comment = payload["comment"]
    sender = comment["user"]["login"]

    if sender.lower() in {ATLAS_MENTION.lower(), CODERABBIT_MENTION.lower()}:
        return {"status": "ignored", "reason": "bot comment"}

    if not contains_atlas_mention(comment["body"]):
        return {"status": "ignored", "reason": "no mention"}

    coderabbit_comment = to_coderabbit_comment(comment["body"])
    owner, repo = payload["repository"]["full_name"].split("/", 1)
    print
    posted = await post_pr_comment(owner, repo, pr_number, coderabbit_comment)

    return {
        "status": "relay_posted",
        "repo": payload["repository"]["full_name"],
        "pr_number": pr_number,
        "source_comment_url": comment["html_url"],
        "posted_comment_url": posted["html_url"],
        "coderabbit_comment": coderabbit_comment,
        "sender": sender,
    }
