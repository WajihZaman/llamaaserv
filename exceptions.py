from fastapi import Request
from fastapi.concurrency import run_in_threadpool
import traceback


# Exception Handling MySQL procedure
def execute_stored_procedure(proc_name: str, params: list, dict_cursor=False):
    """
    Execute a stored procedure in the database.

    Args:
        proc_name (str): Name of the stored procedure.
        params (tuple | list): Parameters to pass to the procedure.
        dict_cursor (bool): Whether to return results as dictionaries.

    Returns:
        list: Rows returned by the stored procedure.
    """

    from central.db import engine
    import pymysql

    conn = engine.raw_connection()
    cursor = None

    # SQLite does not support stored procedures
    if engine.dialect.name == "sqlite":
        return []

    try:
        if dict_cursor:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
        else:
            cursor = conn.cursor()

        cursor.callproc(proc_name, params)

        rows = cursor.fetchall()


        conn.commit()

        return rows

    except Exception:
        conn.rollback()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# send relevant response to user about the error
async def error_details(req: Request, ex: Exception):

    import httpx

    details = str(traceback.format_exc())

    rowsd = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "exceptions.py; in error details function",
            f"Exception:\n{ex} \n\n Details:\n {details}",
        ],
    )

    # Determine status code and user message based on error type
    if isinstance(ex, ValueError):
        status_code = 400
        full_response = "Invalid request. Please check your input."

    elif isinstance(ex, PermissionError):
        status_code = 403
        full_response = "You don't have permission to perform this action."

    elif isinstance(ex, FileNotFoundError):
        status_code = 404
        full_response = "Requested resource was not found."

    elif isinstance(ex, TimeoutError):
        status_code = 504
        full_response = "Request timed out. Please try again."

    elif isinstance(ex, ConnectionError):
        status_code = 503
        full_response = "AI service is temporarily unavailable. Please try again."

    elif isinstance(ex, httpx.ConnectError):
        status_code = 503
        full_response = "Could not connect to AI service. Please try again later."

    elif isinstance(ex, httpx.TimeoutException):
        status_code = 504
        full_response = "AI service took too long to respond. Please try again."

    else:
        status_code = 500
        full_response = "Something went wrong. Please try again later."

    rowsd = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "exceptions.py; in error details function",
            f"Exception for the USER: \n\n status code = {status_code} \n\n full response = {full_response}",
        ],
    )
    return {"status_code": status_code, "resp": full_response}
