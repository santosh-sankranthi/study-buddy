# Phase 1 Instructor Guide: Prompt Engineering

## Learning Objectives
1. Understand the role of system prompts in anchoring persona and constraints.
2. Leverage few-shot demonstrations to enforce rigid formatting.
3. Apply Chain of Thought (CoT) to force intermediate reasoning before answers.
4. Validate structured JSON output using Pydantic models.
5. Grasp tool schemas and the ReAct (Reasoning + Acting) execution paradigm.

## Timing & Pacing (Total: 60 min)
- **1.1 System Prompts (10 min)**: Demo Socratic tutor persona; student adds Flashcard persona.
- **1.2 Few-Shot (10 min)**: Demo MCQ generation; student adapts to fill-in-the-blank.
- **1.3 Chain of Thought (10 min)**: Demo reasoning tags `<thinking>`; student runs math word problem.
- **1.4 Structured Output (15 min)**: Demo Pydantic validation on Flashcard; student creates StudyPlanDay.
- **1.5 Function Calling Concept (8 min)**: Demo tool schemas; student adds calculate_grade schema.
- **1.6 ReAct Concept (7 min)**: Trace Thought/Action/Observation on paper/markdown.

## Live-Coding Narration Tips
- Deliberately run the tutor persona without rules, then add: "Never give the answer directly. Ask ONE guiding question." Show the class how the model's behavior flips instantly.
- In 1.4 Structured Output, show a `ValidationError` when a JSON key is missing to illustrate why Pydantic is production-critical.
