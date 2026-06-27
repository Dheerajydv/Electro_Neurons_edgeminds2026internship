import json


def average(values):
    return round(sum(values) / len(values), 2) if values else 0.0


def observation(acc, ret, faith):
    notes = []

    if acc >= 0.8:
        notes.append("good keyword coverage")
    elif acc >= 0.5:
        notes.append("moderate keyword coverage")
    else:
        notes.append("weak keyword coverage")

    if ret >= 0.8:
        notes.append("strong source retrieval")
    elif ret >= 0.5:
        notes.append("partial source retrieval")
    else:
        notes.append("weak source retrieval")

    if faith >= 0.8:
        notes.append("well grounded")
    elif faith >= 0.5:
        notes.append("partially grounded")
    else:
        notes.append("possible hallucination risk")

    return ", ".join(notes).capitalize() + "."


with open("evaluation_results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

accuracy_scores = [r["accuracy_score"] for r in results]
retrieval_scores = [r["retrieval_score"] for r in results]
faithfulness_scores = [r["faithfulness_score"] for r in results]

avg_accuracy = average(accuracy_scores)
avg_retrieval = average(retrieval_scores)
avg_faithfulness = average(faithfulness_scores)

lines = []
lines.append("# Evaluation Report")
lines.append("")
lines.append("## Overview")
lines.append("")
lines.append(
    "This report summarizes the evaluation of the Autonomous Local Research Agent "
    "on the prepared benchmark dataset."
)
lines.append("")
lines.append("## Aggregate Results")
lines.append("")
lines.append(f"- Total test cases: {len(results)}")
lines.append(f"- Average accuracy score: {avg_accuracy}")
lines.append(f"- Average retrieval score: {avg_retrieval}")
lines.append(f"- Average faithfulness score: {avg_faithfulness}")
lines.append("")
lines.append("## Metric Meaning")
lines.append("")
lines.append("- **Accuracy Score**: Measures expected keyword coverage in the generated report.")
lines.append("- **Retrieval Score**: Measures how many expected source files were retrieved.")
lines.append("- **Faithfulness Score**: Estimates how much the answer is supported by retrieved evidence.")
lines.append("")
lines.append("## Per-topic Results")
lines.append("")
lines.append("| Topic | Accuracy | Retrieval | Faithfulness | Observation |")
lines.append("|---|---:|---:|---:|---|")

for r in results:
    topic = r["topic"]
    acc = round(r["accuracy_score"], 2)
    ret = round(r["retrieval_score"], 2)
    faith = round(r["faithfulness_score"], 2)
    note = observation(acc, ret, faith)

    lines.append(f"| {topic} | {acc} | {ret} | {faith} | {note} |")

lines.append("")
lines.append("## Strengths")
lines.append("")

if avg_faithfulness >= 0.75:
    lines.append("- The system is generally grounded in retrieved local evidence.")
else:
    lines.append("- Faithfulness is inconsistent and needs improvement.")

if avg_accuracy >= 0.75:
    lines.append("- Most responses cover the expected main concepts.")
else:
    lines.append("- Many responses miss expected concepts or keywords.")

if avg_retrieval >= 0.75:
    lines.append("- Retrieval is finding most expected local source files.")
else:
    lines.append("- Retrieval is a major bottleneck and often misses expected files.")

lines.append("")
lines.append("## Weaknesses")
lines.append("")

if avg_retrieval < 0.75:
    lines.append("- Keyword-based retrieval may miss relevant files when wording changes.")

if avg_accuracy < 0.75:
    lines.append("- Answers may be correct in meaning but lose score due to phrasing differences.")

if avg_faithfulness < 0.75:
    lines.append("- Some answers may include unsupported or weakly supported statements.")

lines.append("- The current evaluation is heuristic and not yet a full semantic evaluation.")
lines.append("")
lines.append("## Next Improvements")
lines.append("")
lines.append("- Improve retrieval beyond keyword matching.")
lines.append("- Add per-subquestion evaluation rather than only full-report evaluation.")
lines.append("- Track unsupported claims more precisely.")
lines.append("- Expand the benchmark with harder and lower-evidence cases.")
lines.append("")

with open("evaluation_report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("evaluation_report.md generated successfully.")