"""
(30/03/2026)
Assignment 24: Prompt Engineer

This program demonstrates prompt engineering by comparing weak and strong prompts
across three tasks:
1. Resume creation
2. Business idea generation
3. Study plan development

For each task, the script shows:
- Weak prompt and output
- Strong prompt and output
- Comparison on quality, clarity, relevance, and level of detail
- Prompt element analysis (role, context, constraints, format)

The final section includes key prompting principles, summary findings,
and real-world applications.
"""


def print_heading(title):
	"""Print a clear heading for each major section."""
	print("\n" + "=" * 95)
	print(title)
	print("=" * 95)


def print_subheading(title):
	"""Print a subheading for task-specific sections."""
	print("\n" + "-" * 95)
	print(title)
	print("-" * 95)


def print_comparison_table(comparison):
	"""Print comparison metrics in a table-like format."""
	print("\nComparison (Weak vs Strong Prompt):")
	print(f"{'Metric':<20}{'Weak Prompt Output':<34}{'Strong Prompt Output':<34}")
	print("-" * 88)
	for row in comparison:
		print(f"{row['metric']:<20}{row['weak']:<34}{row['strong']:<34}")


def print_prompt_element_analysis(elements):
	"""Print analysis of prompt engineering elements."""
	print("\nPrompt Element Analysis:")
	for key, value in elements.items():
		print(f"- {key}: {value}")


def print_task(task):
	"""Print full content for one task."""
	print_subheading(f"TASK: {task['task_name']}")

	print("Weak Prompt:")
	print(task["weak_prompt"])

	print("\nOutput for Weak Prompt:")
	print(task["weak_output"])

	print("\nStrong Prompt:")
	print(task["strong_prompt"])

	print("\nOutput for Strong Prompt:")
	print(task["strong_output"])

	print_comparison_table(task["comparison"])
	print_prompt_element_analysis(task["prompt_elements"])

	print("\nWhy Strong Prompt Performs Better:")
	print(task["why_strong_better"])


def print_final_sections():
	"""Print required final discussion sections."""
	print_heading("KEY PRINCIPLES OF EFFECTIVE PROMPTING")
	print("- Clarity: Use clear instructions and avoid vague language.")
	print("- Specificity: Mention exact goals, audience, and expected depth.")
	print("- Context: Provide background information so the model understands purpose.")
	print("- Constraints: Include limits (length, tone, structure, time frame, format).")
	print("- Format Guidance: Ask for bullets, tables, sections, or templates when needed.")

	print_heading("SUMMARY OF FINDINGS")
	print("- Weak prompts gave broad, generic, and less actionable responses.")
	print("- Strong prompts produced clearer, more relevant, and more detailed outputs.")
	print("- Including role + context + constraints improved consistency and usefulness.")
	print("- Prompt structure directly influenced output quality across all three tasks.")

	print_heading("REAL-WORLD USES OF PROMPT ENGINEERING")
	print("- Chatbots: Better user support through precise and context-aware responses.")
	print("- Content Creation: Generate focused articles, ads, scripts, and social posts.")
	print("- Coding: Produce cleaner code snippets, tests, and debugging suggestions.")
	print("- Education: Build personalized study plans, explanations, and practice material.")
	print("- Business: Improve idea generation, strategy drafts, and market analysis.")


def main():
	"""Main function to run the full assignment report."""
	tasks = [
		{
			"task_name": "Resume Creation",
			"weak_prompt": "Write a resume.",
			"weak_output": (
				"Name: Alex\n"
				"Skills: Communication, teamwork\n"
				"Experience: Worked in sales\n"
				"Education: Graduate"
			),
			"strong_prompt": (
				"You are a professional career coach. Create a one-page resume for Priya Sharma, "
				"a final-year B.Tech Computer Science student applying for an entry-level Data Analyst role. "
				"Include sections: Summary, Education, Skills, Projects, Internships, and Certifications. "
				"Keep it concise, ATS-friendly, and use bullet points. Limit to 350 words."
			),
			"strong_output": (
				"PRIYA SHARMA\n"
				"Summary: Final-year B.Tech CSE student with hands-on experience in Python, SQL, and Power BI...\n"
				"Education: B.Tech CSE, ABC Institute, 2022-2026, CGPA: 8.7\n"
				"Skills: Python, SQL, Excel, Power BI, Statistics\n"
				"Projects: Sales Dashboard, Student Performance Prediction\n"
				"Internship: Data Intern at XYZ Analytics (8 weeks)\n"
				"Certifications: Google Data Analytics, NPTEL Python"
			),
			"comparison": [
				{"metric": "Quality", "weak": "Basic and incomplete", "strong": "Professional and polished"},
				{"metric": "Clarity", "weak": "Vague structure", "strong": "Clear section-wise format"},
				{"metric": "Relevance", "weak": "Not role-focused", "strong": "Targeted to Data Analyst role"},
				{"metric": "Level of Detail", "weak": "Very low", "strong": "High and practical"},
			],
			"prompt_elements": {
				"Role": "Career coach persona is defined",
				"Context": "Candidate profile and job target provided",
				"Constraints": "Word limit + ATS-friendly requirement",
				"Format": "Specific resume sections and bullet-point structure",
			},
			"why_strong_better": (
				"The strong prompt gives the model a role, a clear candidate profile, a target job, "
				"and formatting rules, so the response becomes job-specific and usable."
			),
		},
		{
			"task_name": "Business Idea Generation",
			"weak_prompt": "Give me a business idea.",
			"weak_output": "Start an online store and sell products.",
			"strong_prompt": (
				"Act as a startup consultant. Suggest 3 low-investment business ideas for a college student "
				"in Hyderabad with a budget under Rs. 50,000. Include target audience, revenue model, "
				"first 30-day action plan, and one key risk per idea. Use a bullet format."
			),
			"strong_output": (
				"1) Hyperlocal Assignment Printing Service\n"
				"Target: College students near campuses\n"
				"Revenue: Per-page pricing + monthly subscription\n"
				"30-day Plan: Partner with hostels, launch WhatsApp ordering, offer opening discounts\n"
				"Risk: Low margins if pricing is too low\n\n"
				"2) Student Resume + LinkedIn Profile Studio\n"
				"...\n"
				"3) Budget Tiffin Subscription for Hostellers\n"
				"..."
			),
			"comparison": [
				{"metric": "Quality", "weak": "Generic", "strong": "Actionable and realistic"},
				{"metric": "Clarity", "weak": "No structure", "strong": "Organized by idea components"},
				{"metric": "Relevance", "weak": "Broad", "strong": "Matches city, budget, and user"},
				{"metric": "Level of Detail", "weak": "Minimal", "strong": "Step-by-step depth"},
			],
			"prompt_elements": {
				"Role": "Startup consultant role guides strategic output",
				"Context": "Location, user type, and budget constraints provided",
				"Constraints": "3 ideas, budget cap, risk and 30-day plan mandatory",
				"Format": "Bullet-based structured response",
			},
			"why_strong_better": (
				"The strong prompt forces practical recommendations by adding budget, location, "
				"and execution constraints, making ideas realistic instead of generic."
			),
		},
		{
			"task_name": "Study Plan Development",
			"weak_prompt": "Make a study plan for exams.",
			"weak_output": (
				"Study daily for 3 hours. Revise notes and solve questions regularly."
			),
			"strong_prompt": (
				"You are an academic mentor. Create a 4-week study plan for a second-year engineering student "
				"preparing for Data Structures, DBMS, and Operating Systems. Student can study 3 hours on weekdays "
				"and 6 hours on weekends. Include weekly goals, daily time blocks, revision strategy, "
				"practice tests, and burnout prevention tips. Present in a weekly table format."
			),
			"strong_output": (
				"Week 1: Build foundation concepts and short notes\n"
				"Mon-Fri (3 hrs/day): 1 hr DSA + 1 hr DBMS + 1 hr OS\n"
				"Sat-Sun (6 hrs/day): Topic revision + coding practice + mini mock test\n"
				"Week 2-3: Advanced topics + problem-solving\n"
				"Week 4: Full revision + 3 full-length tests + error log review\n"
				"Burnout Tips: 10-minute breaks, one light day per week, sleep before midnight"
			),
			"comparison": [
				{"metric": "Quality", "weak": "Basic advice only", "strong": "Comprehensive and exam-ready"},
				{"metric": "Clarity", "weak": "General", "strong": "Time-blocked and scheduled"},
				{"metric": "Relevance", "weak": "Not subject-specific", "strong": "Tailored to 3 subjects"},
				{"metric": "Level of Detail", "weak": "Low", "strong": "Detailed weekly structure"},
			],
			"prompt_elements": {
				"Role": "Academic mentor persona improves planning quality",
				"Context": "Student level, subjects, and available hours given",
				"Constraints": "4-week timeline + revision + tests + wellness",
				"Format": "Weekly table/time-block expectation",
			},
			"why_strong_better": (
				"The strong prompt transforms a vague request into a practical roadmap by "
				"specifying timeline, subjects, effort limits, and required output format."
			),
		},
	]

	print_heading("ASSIGNMENT: PROMPT ENGINEER")
	print("This report compares weak and strong prompts for three realistic tasks.")

	for task in tasks:
		print_task(task)

	print_final_sections()


if __name__ == "__main__":
	main()
