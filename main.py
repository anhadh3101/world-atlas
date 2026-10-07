from fastapi import FastAPI, Header, Request

from github_utils import relay_mention

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/github/webhooks")
async def handle_webhook(
    request: Request,
    x_github_event: str = Header(alias="X-GitHub-Event"),
):
    payload = await request.json()

    if x_github_event == "ping":
        return {"status": "ok", "event": "ping"}

    if x_github_event == "issue_comment":
        if payload.get("action") != "created":
            return {"status": "ignored", "reason": "not a new comment"}

        issue = payload["issue"]
        if "pull_request" not in issue:
            return {"status": "ignored", "reason": "not a pull request comment"}

        return await relay_mention(payload, issue["number"])

    if x_github_event == "pull_request_review_comment":
        if payload.get("action") != "created":
            return {"status": "ignored", "reason": "not a new comment"}

        return await relay_mention(payload, payload["pull_request"]["number"])

    return {"status": "ok", "event": x_github_event}
