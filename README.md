# Electro Neurons - Autonomous Local Research Agent

A lightweight offline research assistant that:

- breaks a topic into sub-questions,
- searches local documents,
- summarizes evidence-backed findings,
- compiles a final report.

Designed for local deployment with Ollama and a small language model such as `llama3.2:1b`.

## Features

- Offline local document search
- Agentic sub-question planning
- Evidence-based summarization
- Markdown report generation
- JSON evidence export
- Simple modular Python architecture

## Project Structure

```text
ELECTRO_NEURONS_EDGEMINDS2026INTERNSHIP/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── config.py
├── ollama_client.py
├── planner.py
├── retriever.py
├── synthesizer.py
├── reporter.py
├── agent.py
├── utils.py
├── documents/
│   ├── sample1.md
│   └── sample2.txt
└── output/
```

## Setup

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd electro_neurons_local_research_agent
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start Ollama and pull the model:

   ```bash
   ollama pull llama3.2:1b
   ollama serve
   ```

4. Put your `.txt` and `.md` files inside the `documents/` folder.

## Run

```bash
python main.py "impact of climate change on crop yield in India"
```

## Output

After execution, the agent generates:

- `output/final_report.md`
- `output/evidence.json`

## How it works

1. The user provides a research topic.
2. The planner creates sub-questions.
3. The retriever searches local documents for relevant chunks.
4. The synthesizer answers each sub-question using retrieved evidence.
5. The reporter compiles everything into a final report.

## Notes

- The system is designed for offline/local use.
- If the LLM is unavailable, fallback logic still allows basic operation.
- Best results come from well-written local `.txt` and `.md` documents.

## Future Improvements

- Embedding-based retrieval
- Vector database support
- Confidence scoring
- Iterative refinement loop
- Improved agent memory/state tracking
