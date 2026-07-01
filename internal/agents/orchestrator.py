import json

from internal.agents.tools import REGISTRY, TOOL_SCHEMA
from internal.clients.llm import client
from internal.core.config import settings

_MAX_ITERATIONS = 5


async def run_agent(location_name: str, intent: str) -> list[dict]:
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a travel research assistant. "
                f"Find {intent} in {location_name} by searching the web. "
                f"Use the web_search tool to find specific, relevant results from reputable travel websites. "
                f"Search at least twice with different queries to get diverse results."
            ),
        },
        {
            "role": "user",
            "content": f"Find the best {intent} in {location_name}.",
        },
    ]

    accumulated: list[dict] = []

    for _ in range(_MAX_ITERATIONS):
        response = await client.chat.completions.create(
            model=settings.agent_model,
            messages=messages,
            tools=TOOL_SCHEMA,
            tool_choice="auto",
        )

        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))

        if not message.tool_calls:
            break

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if name in REGISTRY:
                results = await REGISTRY[name](**args)
                accumulated.extend(results)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(results),
                    }
                )

    seen: set[str] = set()
    unique: list[dict] = []
    for item in accumulated:
        url = item.get("url", "")
        if url not in seen:
            seen.add(url)
            unique.append(item)

    return unique
