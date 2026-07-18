import re

from llm import ask_llm


def create_plan(user_request: str) -> list:
    planning_prompt = f"""
You are a planning assistant. A user has made the following request:

"{user_request}"

Break this task into a logical TODO list of document sections.
Return ONLY a numbered list of short section titles.
Do not write any content, explanations, or introductions.
Each line must look like: "1. Section Title"

If any important information (like budget or timeline) is missing,
still include a section for it so it can be addressed with assumptions.
""".strip()

    raw_plan_text = ask_llm(planning_prompt)

    plan = _parse_numbered_list(raw_plan_text)

    if not plan:
        plan = ["Introduction", "Details", "Conclusion"]

    return plan


def _parse_numbered_list(text: str) -> list:
    sections = []

    for line in text.split("\n"):
        clean_line = line.replace("*", "").replace("#", "").strip()

        if not clean_line:
            continue

        match = re.match(r"^\d+\s*[.)\-:]?\s*(.+)$", clean_line)

        if match:
            title = match.group(1).strip()
            if title:
                sections.append(title)

    return sections