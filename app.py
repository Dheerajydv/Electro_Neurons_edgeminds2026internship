from flask import Flask, render_template, request, jsonify
from agent import run_agent
import json

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "Autonomous Local Research Agent backend is running."
    })


@app.route("/run", methods=["POST"])
def run():
    try:
        data = request.get_json(silent=True) or {}
        topic = (data.get("topic") or "").strip()

        if not topic:
            return jsonify({
                "topic": "",
                "report": "",
                "raw": None,
                "error": "Topic is required."
            }), 400

        result = run_agent(topic)

        if isinstance(result, dict):
            candidate = (
                result.get("report")
                or result.get("final_report")
                or result.get("answer")
                or result.get("answers")
            )

            if isinstance(candidate, dict):
                report_text = json.dumps(candidate, indent=2, ensure_ascii=False)
            elif isinstance(candidate, list):
                report_text = json.dumps(candidate, indent=2, ensure_ascii=False)
            elif candidate is not None:
                report_text = str(candidate)
            else:
                report_text = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            report_text = str(result)

        return jsonify({
            "topic": topic,
            "report": report_text,
            "raw": result,
            "error": None
        }), 200

    except Exception as e:
        return jsonify({
            "topic": "",
            "report": "",
            "raw": None,
            "error": f"{type(e).__name__}: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)