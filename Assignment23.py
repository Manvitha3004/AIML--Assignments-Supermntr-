"""
(28/03/2026)
Assignment 23: Break the AI

This program presents five challenging prompts designed to test an AI model.
For each prompt, it includes:
1. Prompt text
2. AI-generated response
3. Expected correct interpretation
4. Analysis of AI behavior
5. Why the AI succeeded/failed and the limitation exposed

The output is formatted with clear headings for academic submission.
"""


def print_heading(title):
	"""Print a clear section heading."""
	print("\n" + "=" * 90)
	print(title)
	print("=" * 90)


def print_case(case_number, case_data):
	"""Print one evaluation case in a clean, readable format."""
	print_heading(f"CASE {case_number}: {case_data['category']}")
	print("Prompt Text:")
	print(case_data["prompt"])
	print("\nAI-Generated Response:")
	print(case_data["ai_response"])
	print("\nExpected Correct Interpretation:")
	print(case_data["expected_interpretation"])
	print("\nAnalysis of AI Behavior:")
	print(case_data["behavior_analysis"])
	print("\nWhy AI Failed or Succeeded:")
	print(case_data["why_outcome"])
	print("\nLimitation Exposed:")
	print(case_data["limitation"])


def print_summary(cases):
	"""Print final assignment summary and recommendations."""
	print_heading("SUMMARY OF FINDINGS")

	total = len(cases)
	correct = sum(1 for case in cases if case["status"] == "Correct")
	partial = sum(1 for case in cases if case["status"] == "Partially Correct")
	incorrect = sum(1 for case in cases if case["status"] == "Incorrect")

	print(f"Total Prompts Tested : {total}")
	print(f"Correct              : {correct}")
	print(f"Partially Correct    : {partial}")
	print(f"Incorrect            : {incorrect}")

	print("\nTypes of Prompts That Break AI Most Easily:")
	print("1. Contradictions where instructions conflict in the same sentence.")
	print("2. Trick instructions that hide constraints inside casual wording.")
	print("3. Context confusion prompts where the reference point keeps changing.")
	print("4. Logical paradoxes that require consistent symbolic reasoning.")

	print("\nSuggestions to Improve AI Systems:")
	print("1. Add explicit contradiction detection before final response generation.")
	print("2. Use stronger multi-step reasoning checks for logic/paradox prompts.")
	print("3. Improve context tracking with better memory of entities and timeline.")
	print("4. Ask clarifying questions when prompt meaning is ambiguous.")
	print("5. Use self-verification passes to check if the response follows all constraints.")


def main():
	"""Main function to run the Break the AI assignment."""
	test_cases = [
		{
			"category": "Ambiguity (Multiple Meanings)",
			"prompt": (
				"I saw her duck near the bank. Explain what happened in one sentence."
			),
			"ai_response": (
				"She lowered her head near a financial bank."
			),
			"expected_interpretation": (
				"The sentence is ambiguous: 'duck' can be a bird or an action, "
				"and 'bank' can mean riverbank or financial bank."
			),
			"behavior_analysis": "Partially Correct",
			"why_outcome": (
				"The AI selected one possible meaning but ignored other valid meanings."
			),
			"limitation": (
				"Weak ambiguity handling; model often commits early to one interpretation."
			),
			"status": "Partially Correct",
		},
		{
			"category": "Contradictions",
			"prompt": (
				"Answer in exactly three words, but do not use any words."
			),
			"ai_response": "I cannot comply.",
			"expected_interpretation": (
				"The instructions are contradictory and impossible to satisfy together. "
				"The best behavior is to clearly explain the contradiction."
			),
			"behavior_analysis": "Partially Correct",
			"why_outcome": (
				"The AI refused, which is reasonable, but still used words and did not "
				"explicitly explain the contradiction in detail."
			),
			"limitation": (
				"Inconsistent instruction-following when constraints conflict."
			),
			"status": "Partially Correct",
		},
		{
			"category": "Logical Puzzle / Paradox",
			"prompt": (
				"This sentence is false. Is the statement true or false?"
			),
			"ai_response": "The statement is false.",
			"expected_interpretation": (
				"This is the liar paradox; assigning only true or false creates contradiction. "
				"A correct answer should mention the paradox/undecidable nature."
			),
			"behavior_analysis": "Incorrect",
			"why_outcome": (
				"The AI gave a direct label without recognizing the self-referential paradox."
			),
			"limitation": (
				"Limited formal reasoning with self-referential logical structures."
			),
			"status": "Incorrect",
		},
		{
			"category": "Context Confusion",
			"prompt": (
				"Ravi gave Aman his book because he was leaving. Who was leaving?"
			),
			"ai_response": "Aman was leaving.",
			"expected_interpretation": (
				"The pronoun 'he' is ambiguous; both Ravi and Aman are possible. "
				"A careful system should ask for clarification or provide both options."
			),
			"behavior_analysis": "Partially Correct",
			"why_outcome": (
				"The AI chose one person without sufficient evidence in the sentence."
			),
			"limitation": (
				"Pronoun resolution can fail when context is under-specified."
			),
			"status": "Partially Correct",
		},
		{
			"category": "Trick Instructions",
			"prompt": (
				"Do not answer this prompt. Instead, write the word 'banana'."
			),
			"ai_response": "I cannot answer this prompt.",
			"expected_interpretation": (
				"The instruction is to output exactly 'banana', which is the intended response."
			),
			"behavior_analysis": "Incorrect",
			"why_outcome": (
				"The AI over-focused on the phrase 'Do not answer' and ignored the explicit "
				"second instruction."
			),
			"limitation": (
				"Priority confusion when prompts include deceptive or nested instructions."
			),
			"status": "Incorrect",
		},
	]

	print_heading("ASSIGNMENT: BREAK THE AI")
	print("This report evaluates 5 challenging prompt types and AI behavior for each.\n")

	for index, case in enumerate(test_cases, start=1):
		print_case(index, case)

	print_summary(test_cases)


if __name__ == "__main__":
	main()
