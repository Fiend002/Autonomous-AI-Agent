from llm import ask_llm


def execute_plan(user_request: str, plan: list) -> list:
    results = []

    for index, section_title in enumerate(plan, start=1):
        section_prompt = f"""
The overall task is: "{user_request}"

Write the content for ONLY the following section of the document:
Section: "{section_title}"

Rules:
- Write clear, professional, well-structured content.
- Do NOT repeat the section title as a heading (it is added separately).
- If some required information is missing (for example budget or
  timeline), make a reasonable assumption and clearly state it.
- Keep it concise but complete (a few short paragraphs or bullet points).
""".strip()

        try:
            section_content = ask_llm(section_prompt)
        except Exception as error:
            section_content = (
                f"[This section could not be generated due to an error: {error}]"
            )

        results.append(
            {
                "title": section_title,
                "content": section_content,
            }
        )

        print(f"  ✓ Completed section {index}/{len(plan)}: {section_title}")

    return results