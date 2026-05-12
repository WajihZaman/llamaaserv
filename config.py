from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
import subprocess
import os
import platform
import asyncio

# debug
from exceptions import execute_stored_procedure
from fastapi.concurrency import run_in_threadpool


# Global holder for the model
ai_server_process = None
sys_check: asyncio.Task | None = None
cmd = None


async def sys_checker():
    global ai_server_process, cmd

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "config.py; before lifespan",
            "inside sys checker function; ai server process check",
        ],
    )

    while True:
        rows = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "config.py; before lifespan",
                "inside sys checker function; while loop",
            ],
        )
        await asyncio.sleep(300)
        try:
            if cmd:
                rows = await run_in_threadpool(
                    execute_stored_procedure,
                    "fastapi_add_logs",
                    [
                        "dev_tester",
                        "CAM laptop",
                        "config.py; before lifespan",
                        "inside sys checker function; cmd check complete... performing app check",
                    ],
                )
                if ai_server_process is None or ai_server_process.poll() is not None:
                    rows = await run_in_threadpool(
                        execute_stored_procedure,
                        "fastapi_add_logs",
                        [
                            "dev_tester",
                            "CAM laptop",
                            "config.py; before lifespan",
                            "inside sys checker function; app idle - asleep. waking it up...",
                        ],
                    )

                    ai_server_process = subprocess.Popen(
                        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
                    )
                    await asyncio.sleep(300)
        except Exception as ex:
            rows = await run_in_threadpool(
                execute_stored_procedure,
                "fastapi_add_logs",
                [
                    "dev_tester",
                    "CAM laptop",
                    "config.py; before lifespan",
                    f"inside sys checker function; in server start exception - logged: {ex}",
                ],
            )

            pass


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Base.metadata.create_all(bind=engine)
    # used to create mysql tables on startup. but user id does not have the priviledges so it is no longer required.

    # debug
    from exceptions import execute_stored_procedure
    from fastapi.concurrency import run_in_threadpool
    import traceback

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "config.py; in lifespan",
            "inside lifespan function",
        ],
    )

    global ai_server_process  # acesses the server_process above so that its value is also updated and accessible to the yield section on app shutdown

    try:
        # 1. Detect the Operating System
        rows = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            ["dev_tester", "CAM laptop", "config.py; in lifespan", "inside try block"],
        )

        system_type = platform.system()  # Returns "Windows", "Linux", or "Darwin"
        # 2. Pick the right file name
        if system_type == "Windows":
            rows = await run_in_threadpool(
                execute_stored_procedure,
                "fastapi_add_logs",
                [
                    "dev_tester",
                    "CAM laptop",
                    "config.py; in lifespan",
                    "inside Windows",
                ],
            )
            exe_name = "llama-server.exe"
            ai_eng_path = os.path.abspath(f"./bin2/{exe_name}")
            # print(f"Selected WINDOW AI Engine: {exe_name}")
        else:
            exe_name = "llama-server"  # Works for Ubuntu/Linux
            ai_eng_path = os.path.abspath(f"./bin/{exe_name}")
            rows = await run_in_threadpool(
                execute_stored_procedure,
                "fastapi_add_logs",
                ["dev_tester", "CAM laptop", "config.py; in lifespan", "inside linux"],
            )

        model_path = os.path.abspath("./models/cam-assistant.gguf")

        if system_type != "Windows":
            # print(f"Applying execution permissions to {exe_name}...")
            os.chmod(ai_eng_path, 0o755)
            rowsd = await run_in_threadpool(
                execute_stored_procedure,
                "fastapi_add_logs",
                [
                    "dev_tester",
                    "CAM laptop",
                    "config.py; in lifespan",
                    "applying executive permission to linux",
                ],
            )

        global cmd

        cmd = [
            ai_eng_path,
            "-m",
            model_path,
            "--port",
            "5001",
            "-t",
            "5",
            "--host",
            "127.0.0.1",
            "-c",
            "2048",
            "-np",
            "2",
            "--cont-batching",
            "--mlock",
        ]

        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "config.py; in lifespan",
                "command ready for model: cmd",
            ],
        )

        # On Linux, we don't need creationflags

        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "config.py; in lifespan",
                "AI server process - start",
            ],
        )

        ai_server_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,  # Important: returns strings instead of bytes
        )

        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "config.py; in lifespan",
                "Server process complete. Going to sleep for model load to RAM.",
            ],
        )

        # Wait for the model to load into RAM

        # import asyncio

        await asyncio.sleep(60)
        # time.sleep(12)
        # print("AI Engine is ready.")
        if ai_server_process.poll() is not None:
            # The process has already exited (crashed)
            ai_startup_error_log = (
                ai_server_process.stdout.read()
                if ai_server_process.stdout
                else "No output captured"
            )
            rowsd = await run_in_threadpool(
                execute_stored_procedure,
                "fastapi_add_logs",
                [
                    "dev_tester",
                    "CAM laptop",
                    "config.py; in lifespan",
                    f"AI Engine Crashed: {ai_startup_error_log}!",
                ],
            )

        else:
            global sys_check
            sys_check = asyncio.create_task(sys_checker())
            rowsd = await run_in_threadpool(
                execute_stored_procedure,
                "fastapi_add_logs",
                [
                    "dev_tester",
                    "CAM laptop",
                    "config.py; in lifespan",
                    "Sleep complete. AI Engine appears to be running!",
                ],
            )

    except Exception as appup:
        details = str(traceback.format_exc()) or "N/A"

        rowsd = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "config.py; in lifespan",
                f"In exception part. \n Exception: {appup} \n\n {details} ",
            ],
        )

    yield

    # dev
    from services.dbops import execute_stored_procedure
    from fastapi.concurrency import run_in_threadpool

    # global sys_check

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "config.py; in lifespan",
            "inside yield; Closing system check.",
        ],
    )

    if sys_check:
        sys_check.cancel()
        try:
            await sys_check
        except asyncio.CancelledError:
            pass

    if ai_server_process:
        # print("Shutting down AI Engine...")
        rows = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "config.py; in lifespan",
                "inside yield; shutting down AI.",
            ],
        )

        ai_server_process.terminate()  # Ask nicely to stop
        try:
            # Wait up to 5 seconds for it to exit
            ai_server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # print("AI Engine hung, forcing kill...")
            rows = await run_in_threadpool(
                execute_stored_procedure,
                "fastapi_add_logs",
                [
                    "dev_tester",
                    "CAM laptop",
                    "config.py; in lifespan",
                    "inside yield; in except block; AI hung. forcing kill",
                ],
            )
            ai_server_process.kill()  # Force it to stop


load_dotenv()
