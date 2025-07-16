from fastapi import FastAPI, Request, Response, HTTPException
import httpx, os

app = FastAPI(title="Python API?Gateway")
TASK_URL  = os.getenv("TASK_URL",  "http://task-service:4001")
TIMER_URL = os.getenv("TIMER_URL", "http://timer-service:4002")

client = httpx.AsyncClient()

# simple mapping table
ROUTES = {
    "/api/tasks":      (TASK_URL,  "/tasks"),
    "/api/tasks/":     (TASK_URL,  "/tasks/"),
    "/api/timer":      (TIMER_URL, "/timer"),
    "/api/timer/":     (TIMER_URL, "/timer/"),
}

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PATCH"])
async def proxy(full_path: str, request: Request):
    path = "/" + full_path

    for prefix, (base, target_prefix) in ROUTES.items():
        if path.startswith(prefix):
            # -------------------------------------------------------------
            # OLD version (buggy):
            #   upstream = base + path.removeprefix(prefix).rjust(1, "/")
            #
            # NEW: keep the suffix **and** add the service’s target_prefix
            # -------------------------------------------------------------
            suffix = path[len(prefix):]             # "" or "/123"
            upstream = f"{base}{target_prefix}{suffix}"
            # -------------------------------------------------------------
            try:
                resp = await client.request(
                    request.method,
                    upstream,
                    content=await request.body(),
                    headers={
                        k: v for k, v in request.headers.items()
                        if k.lower() != "host"
                    },
                )
                return Response(
                    content=resp.content,
                    status_code=resp.status_code,
                    headers=resp.headers,
                )
            except httpx.RequestError as exc:
                raise HTTPException(502, f"upstream error: {exc}") from exc

    raise HTTPException(404, "no route")
