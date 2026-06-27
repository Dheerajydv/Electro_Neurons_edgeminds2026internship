import json
from agent import run_agent


def keyword_score(text, keywords):
    text = str(text).lower()
    found = 0

    for keyword in keywords:
        if keyword.lower() in text:
            found += 1

    return found / max(len(keywords), 1)


def retrieval_score(evidence_map, expected_sources):
    retrieved_files = set()

    for evidences in evidence_map.values():
        for e in evidences:
            filename = e["file"].replace("\\", "/").split("/")[-1]
            retrieved_files.add(filename)

    expected_files = set(expected_sources)
    matched = len(expected_files.intersection(retrieved_files))

    return matched / max(len(expected_files), 1)


def faithfulness_score(answer, evidences):
    evidence_text = " ".join(
        e.get("snippet", "").lower()
        for e in evidences
    )

    answer_words = set(str(answer).lower().split())

    matched = 0
    for word in answer_words:
        if word in evidence_text:
            matched += 1

    return matched / max(len(answer_words), 1)


with open("evaluation_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)


results = []

for case in dataset:
    print(f"Running: {case['topic']}")

    result = run_agent(case["topic"])

    if isinstance(result, dict):
        report = result.get("report") or result.get("answers") or json.dumps(result, ensure_ascii=False)
    else:
        report = str(result)

    with open("output/evidence.json", "r", encoding="utf-8") as f:
        evidence_map = json.load(f)

    accuracy = keyword_score(
        report,
        case["expected_keywords"]
    )

    retrieval = retrieval_score(
        evidence_map,
        case["expected_sources"]
    )

    faithfulness_scores = []

    for question, evidences in evidence_map.items():
        score = faithfulness_score(
            report,
            evidences
        )
        faithfulness_scores.append(score)

    faithfulness = (
        sum(faithfulness_scores) / len(faithfulness_scores)
        if faithfulness_scores else 0
    )

    print("Accuracy =", accuracy)
    print("Retrieval =", retrieval)
    print("Faithfulness =", faithfulness)

    results.append({
        "topic": case["topic"],
        "accuracy_score": accuracy,
        "retrieval_score": retrieval,
        "faithfulness_score": faithfulness
    })

with open("evaluation_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("Evaluation completed.")