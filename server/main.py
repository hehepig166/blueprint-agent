# Config must be at the top
from config import settings

import asyncio
import json
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.logger import logger

from agents import LeanSearchAgent
from kernel import OpenAIProvider
from .schemas import Stage
from .utils import result_to_json

app = FastAPI(root_path="/api/v1")

# init ai provider
llm_provider = OpenAIProvider(
    model=settings.MODEL_NAME,
    base_url=settings.OPENAI_BASE_URL,
    api_key=settings.OPENAI_API_KEY,
)


def stream_json(stage: Stage, data: dict, msg: str | None = None):
    """Stream json response to client"""
    payload = {"stage": stage.value, "msg": msg, "data": data}
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


async def processor(
    search_agent: LeanSearchAgent,
    q: str,
    limit: int,
    generate_query: bool,
    analyze_result: bool,
):
    data = {
        "user_query": q,
        "agent_query": None,
        "search_results": None,
        "analysis": None,
        "analysis_text": None,
        "cover_match": None,
    }

    # Stage1: generate agent query
    if generate_query:
        try:
            data["agent_query"] = await asyncio.to_thread(
                search_agent.generate_search_query, q
            )
        except Exception as e:
            logger.exception("Failed to generate search query: %s", e)
            yield stream_json(
                Stage.GENERATE_QUERY, data, f"Query generation failed: {e}"
            )
            return

        if data["agent_query"] == "NO_SEARCH":
            yield stream_json(
                Stage.GENERATE_QUERY, data, "No search needed for this query"
            )
            return
        yield stream_json(Stage.GENERATE_QUERY, data)
    else:
        # If not generating query, use the original query
        data["agent_query"] = q
        yield stream_json(
            Stage.GENERATE_QUERY, data, "Using original query (skip generation)"
        )

    # Stage2: Perform search for lean explore
    try:
        search_results = await search_agent.search_lean_explore(
            data["agent_query"], limit
        )
        data["search_results"] = [_.model_dump() for _ in search_results]
    except Exception as e:
        logger.exception("Search failed: %s", e)
        yield stream_json(Stage.SEARCH, data, f"Search failed: {e}")
        return

    if not data["search_results"]:
        yield stream_json(Stage.SEARCH, data, "No result found")
        return
    yield stream_json(Stage.SEARCH, data)

    # Stage3: Analyze search results
    if not analyze_result:
        return

    try:
        analysis = await asyncio.to_thread(
            search_agent.analyze_search_results,
            q,
            data["agent_query"],
            search_results,
        )
    except Exception as e:
        logger.exception("Analysis failed: %s", e)
        yield stream_json(Stage.ANALYZE, data, f"Analysis failed: {e}")
        return

    data["analysis_text"] = analysis
    data["analysis"] = result_to_json(analysis)

    # Extract cover match from analysis (simple parsing)
    for line in analysis.splitlines():
        if "Cover match" in line and ":" in line:
            val = line.split(":", 1)[1].strip().strip("`")
            data["cover_match"] = None if val == "None" else val
            break

    yield stream_json(Stage.ANALYZE, data)


@app.get("/search")
async def search(
    q: str = Query(..., description="The user's mathematical question or statement"),
    limit: int = Query(
        50, ge=1, description="Maximum number of search results to return"
    ),
    generate_query: bool = Query(True, description="Whether to generate a new query"),
    analyze_result: bool = Query(
        True, description="Whether to analyze the lean explore search results"
    ),
):
    search_agent = LeanSearchAgent(llm_provider)
    return StreamingResponse(
        processor(search_agent, q, limit, generate_query, analyze_result),
        media_type="text/event-stream",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
