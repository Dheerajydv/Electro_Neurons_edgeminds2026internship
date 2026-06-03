# ELECTRO_NEURONS_EDGE_MINDS_HACKATHON

## Autonomous Local Research Agent

## Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start Ollama and pull model:
   ```bash
   ollama pull llama3.2:1b
   ollama serve
   ```
3. Put files in `documents/`.
4. Run:
   ```bash
   python main.py "your topic"
   ```

## Output

- `output/final_report.md`
- `output/evidence.json`
