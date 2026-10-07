import os

import httpx
from fastapi import HTTPException

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


async def post_pr_comment(owner: str, repo: str, pr_number: int, body: str) -> dict:
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="GITHUB_TOKEN is not configured")

    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"body": body}, headers=headers)

    if response.status_code >= 400:
        raise HTTPException(
            status_code=502,
            detail=f"GitHub API error: {response.status_code} {response.text}",
        )

    return response.json()
