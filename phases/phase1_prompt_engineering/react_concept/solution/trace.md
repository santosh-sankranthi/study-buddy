# ReAct Hand Trace

Thought: I need to find today's date first.
Action: get_current_date()
Observation: Today is 2026-09-28.

Thought: Now I need to calculate how many days remain until the Algorithms exam on 2026-11-01.
Action: calculate_days_between(start="2026-09-28", end="2026-11-01")
Observation: 34 days remaining.

Thought: I have the date and countdown. Now I should search the student's notes for key algorithms topics.
Action: search_notes(query="algorithms exam topics")
Observation: Found topics: Dynamic Programming, Graph Traversals (BFS/DFS), Greedy Algorithms.

Thought: I now have all necessary information to construct the complete answer.
Action: FINISH(answer="Your Algorithms exam is in 34 days (Nov 1). Key topics from your notes to review: Dynamic Programming, BFS/DFS, and Greedy Algorithms.")
