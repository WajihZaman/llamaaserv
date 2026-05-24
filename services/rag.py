
from central.prompts import system_prompt
from central.schema import UserQuery
from central.common import url
from services.dbops import get_or_create_history, save_chat
import httpx

# debug
from exceptions import execute_stored_procedure
from fastapi.concurrency import run_in_threadpool


async def respond_to_chat(objMsg: UserQuery):

    convo_id = str(objMsg.convo_id)
    msg = objMsg.msg

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "rag.py; in respond_to_chat",
            "in respond_to_chat; msg & convo_id ready",
        ],
    )

    from central.common import collection_name

    
    context_data = await search_similar_chunks(msg, collection_name)  # type: ignore

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "rag.py; in respond_to_chat",
            "in respond_to_chat; context data ready",
        ],
    )

    messages = [{"role": "system", "content": system_prompt}]

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "rag.py; in respond_to_chat",
            "in respond_to_chat; in messages",
        ],
    )

    history = await get_or_create_history(convo_id=convo_id)

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "rag.py; in respond_to_chat",
            "in respond_to_chat; got history",
        ],
    )

    # Add the retrieved history turns
    if history:
        messages.extend(history)
        rows = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "rag.py; in respond_to_chat",
                "in respond_to_chat; history added to messages",
            ],
        )

    # Add the current User Query + Context Data from your Vector DB
    current_input = f"# Context Data: {context_data} \n\n # User Query: {msg}"

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "rag.py; in respond_to_chat",
            "in respond_to_chat; current input ready",
        ],
    )

    messages.append(
        {"role": "user", "content": current_input}
    )  # remove t from current_imput

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "rag.py; in respond_to_chat",
            "in respond_to_chat; current input added to messages",
        ],
    )

    
    payload = {
        "model": "cam-assistant",
        "messages": messages,
        "stream": False,
        "max_tokens": 800,
        "temperature": 0.0,
    }  # remove [] from payload

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "rag.py; in respond_to_chat",
            "in respond_to_chat; payload ready",
        ],
    )

    

    full_response = ""

    async with httpx.AsyncClient(timeout=None) as client:
        rows = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "rag.py; in respond_to_chat",
                "in respond_to_chat; Async Client",
            ],
        )

        # Use a standard post() instead of stream()
        response = await client.post(url, json=payload)

        rows = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "rag.py; in respond_to_chat",
                "in respond_to_chat; response given to payload from Client.",
            ],
        )

        

        if response.status_code != 200:
            # This triggers your exception block for logging
            rows = await run_in_threadpool(
                execute_stored_procedure,
                "fastapi_add_logs",
                [
                    "dev_tester",
                    "CAM laptop",
                    "rag.py; in respond_to_chat",
                    "in respond_to_chat; response not 200! exception raised",
                ],
            )
            response.raise_for_status()

        result = response.json()
        rows = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "rag.py; in respond_to_chat",
                "in respond_to_chat; response json added to results",
            ],
        )

        

        full_response = (
            result.get("choices", [{}])[0].get("message", {}).get("content", "")
        )

        rows = await run_in_threadpool(
            execute_stored_procedure,
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "rag.py; in respond_to_chat",
                "in respond_to_chat; full response ready.",
            ],
        )

        if full_response:
            rows = await run_in_threadpool(
                execute_stored_procedure,
                "fastapi_add_logs",
                [
                    "dev_tester",
                    "CAM laptop",
                    "rag.py; in respond_to_chat",
                    "in respond_to_chat; full response saved to chat.",
                ],
            )
            await save_chat(full_response, objMsg)

        return {"status_code": 200, "resp": full_response}

        # return full_response


async def search_similar_chunks(query: str, collection_name: str, k: int = 3):

    from central.common import chromaclient

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        ["dev_tester", "CAM laptop", "rag.py; in search chunks", "in search chunks; "],
    )

    inputs = "Represent this sentence for searching relevant passages: " + query
    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "rag.py; in search chunks",
            "in search chunks; input ready",
        ],
    )

    collection = chromaclient.get_collection(name=collection_name)

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "rag.py; in search chunks",
            "in search chunks; collection ready",
        ],
    )

    results = collection.query(query_texts=[inputs], n_results=k)

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "rag.py; in search chunks",
            "in search chunks; chroma results ready",
        ],
    )

    

    documents = results.get("documents", [[]])  # Get the text list

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "rag.py; in search chunks",
            "in search chunks; documents ready.",
        ],
    )

    

    if not documents or not documents[0]:
        context_text = ""
    else:
        context_text = "\n\n".join(documents[0])

    

    rows = await run_in_threadpool(
        execute_stored_procedure,
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "rag.py; in search chunks",
            "in search chunks; context text from documents ready.",
        ],
    )

    

    return context_text

    
