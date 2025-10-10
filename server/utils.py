import re

_result_pattern = re.compile(
    r"\*\*(\d+)\. [^\*]+\*\*\n"
    r"- \*\*Lean Name\*\*: `([^`]+)`\n"
    r"- \*\*Type\*\*: ([^\n]+)\n"
    r"- \*\*Statement\*\*: `([^`]+)`\n"
    r"- \*\*Relevance\*\*: ([^\n]+)\n"
    r"- \*\*Module\*\*: ([^\n]+)\n"
    r"(?:- \*\*Documentation\*\*: ([^\n]+))?",
    flags=re.MULTILINE
)


def result_to_json(text: str) -> list[dict]:
    results = []
    for match in _result_pattern.findall(text):
        idx, lean_name, typ, statement, relevance, module, doc = match
        results.append(
            {
                "index": int(idx),
                "lean_name": lean_name.strip(),
                "type": typ.strip(),
                "statement": statement.strip(),
                "relevance": relevance.strip(),
                "module": module.strip(),
                "documentation": (
                    None
                    if not doc or doc.strip() == "(No docstring provided)"
                    else doc.strip()
                ),
            }
        )
    return results
