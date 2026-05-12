from central.db import AppUsers
from central.schema import UserQuery
from central.db import SessionLocal
from datetime import datetime, timezone

# debug
from exceptions import execute_stored_procedure
from fastapi.concurrency import run_in_threadpool


async def get_or_create_history(convo_id: str):

    rowsd = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        ["dev_tester", "CAM laptop", "dbops.py", "in get history function; "],
    )

    today_start = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    rowsd = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "dbops.py",
            "in get history function; today date ready",
        ],
    )

    with SessionLocal() as db:
        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "dbops.py",
                "in get history function; session local ready",
            ],
        )

        rows = (
            db.query(AppUsers)
            .filter(
                AppUsers.convo_id == convo_id,
                AppUsers.chat_date >= today_start,
            )
            .order_by(AppUsers.serial_no.asc())
            .all()
        )

        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "dbops.py",
                "in get history function; rows ready",
            ],
        )

        convo_history = []

        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "dbops.py",
                "in get history function; extracting convo history.",
            ],
        )

        for r in rows:
            request = r.request.encode("utf-8").decode("unicode_escape")
            response = r.response.encode("utf-8").decode("unicode_escape")
            convo_history.append({"role": "user", "content": request})
            convo_history.append({"role": "system", "content": response})

        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "dbops.py",
                "in get history function; sending convo history",
            ],
        )

        # Returns empty list [] if no history exists (matches your logic)
        return convo_history


async def save_chat(resp: str, new_data: UserQuery):
    # Update MySQL with the NEW turn (Query + Response)

    rowsd = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        ["dev_tester", "CAM laptop", "dbops.py", "in save chat function; "],
    )

    appusers_row = AppUsers(
        uid=str(new_data.uid),  # str converts 32 bit uuid to 36 bit by adding dashes
        emp_no=new_data.emp_no,
        convo_id=new_data.convo_id,
        request=new_data.msg,
        response=resp,
    )

    rowsd = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "dbops.py",
            "in save chat function; appusers row ready",
        ],
    )

    # user_msg, bot_msg,
    with SessionLocal() as db:
        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "dbops.py",
                "in save chat function; saving chat to DB.",
            ],
        )
        db.add(appusers_row)
        db.commit()
