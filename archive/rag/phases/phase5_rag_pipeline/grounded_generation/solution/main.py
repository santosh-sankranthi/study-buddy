"""SOLUTION -- Citations and Grounded RAG Prompts."""
def build_rag_prompt_with_sources(question: str, chunks: list[dict]) -> str:
    parts = ["Context Notes:"]
    for c in chunks:
        fn = c.get("metadata", {}).get("filename", "unknown.md")
        parts.append(f"[Source: {fn}]\n{c.get('text', '')}\n[End Source]")
    parts.append(f"\nStudent Question: {question}")
    parts.append("Answer the question using only the context notes above. Cite the source filename.")
    return "\n".join(parts)

if __name__ == "__main__":
    print(build_rag_prompt_with_sources("test", [{"text": "note", "metadata": {"filename": "a.md"}}]))
