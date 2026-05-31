from config import lifespan
from services.rag import respond_to_chat
from services.security import get_current_user
from fastapi import Depends, FastAPI, Body, Request  
from typing import Annotated, Optional
from central.schema import UserQuery
import uvicorn

# Absolute Execution Tracing code
from exceptions import execute_stored_procedure, error_details
from fastapi.concurrency import run_in_threadpool

app = FastAPI(lifespan=lifespan)

rowsd = execute_stored_procedure(
    "fastapi_add_logs",
    ["dev_tester", "CAM laptop", "main file; in /get_context", " inside fastapi"],
)


@app.post("/get_context")
async def get_context(
    request: Request,
    uid_hashed: Annotated[str, Depends(get_current_user)],
    data: Optional[UserQuery] = Body(None),
    rows=execute_stored_procedure(
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "main file; calling /get_context",
            " inside get context api",
        ],
    ),
):  

    rowsd = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "main file; in /get_context",
            " inside get context function",
        ],
    )

    if data is None:
        return "Hi. How can I help you?"

    rowsd = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        ["dev_tester", "CAM laptop", "main file; in /get_context", " got data"],
    )

    try:
        captured_user_data = {"emp_no": data.emp_no, "msg": data.msg}

        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "main file; /get_context;",
                f"got captured data; in try block: \n {captured_user_data}",
            ],
        )

        data.convo_id = uid_hashed
        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "main file; in /get_context",
                f"convo ID set:\n {uid_hashed} \n call respond to chat",
            ],
        )

        resp = await respond_to_chat(data)

        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "main file; in /get_context",
                f"got response:\n {resp}",
            ],
        )

        return resp

    except Exception as ex:
        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "main file; in /get_context",
                f"except block.\n Exception: {ex}",
            ],
        )

        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "main file; in /get_context",
                "Calling error details to record exception",
            ],
        )

        resp = await error_details(request, ex)

        return resp


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="127.0.0.1", port=8000, reload=True, server_header=False
    )
