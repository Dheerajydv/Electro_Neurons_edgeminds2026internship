document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("research-form");
  const submitBtn = document.getElementById("submit-btn");
  const copyBtn = document.getElementById("copy-btn");
  const reportContent = document.getElementById("report-content");
  const topicField = document.getElementById("topic");
  const topicOutput = document.getElementById("topic-output");
  const errorBox = document.getElementById("error-box");
  const errorText = document.getElementById("error-text");

  function showError(message) {
    if (errorBox && errorText) {
      errorText.textContent = message;
      errorBox.style.display = "block";
    }
  }

  function hideError() {
    if (errorBox) errorBox.style.display = "none";
    if (errorText) errorText.textContent = "";
  }

  function renderMarkdown(markdownText) {
    if (!reportContent) return;

    if (typeof markdownText === "object" && markdownText !== null) {
      markdownText = JSON.stringify(markdownText, null, 2);
    }

    const safeText = markdownText || "No report generated.";

    if (window.marked) {
      reportContent.innerHTML = marked.parse(safeText);
    } else {
      reportContent.textContent = safeText;
    }
  }

  if (form) {
    form.addEventListener("submit", async function (event) {
      event.preventDefault();

      const topic = topicField ? topicField.value.trim() : "";
      if (!topic) {
        alert("Please enter a research topic.");
        return;
      }

      hideError();

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Running Agent...";
        submitBtn.classList.add("loading");
      }

      if (topicOutput) {
        topicOutput.textContent = topic;
      }

      if (reportContent) {
        reportContent.innerHTML = "<p>Running local research agent...</p><p>Please wait while the report is generated.</p>";
      }

      try {
        const response = await fetch("/run", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ topic: topic })
        });

        const rawText = await response.text();

        let data;
        try {
          data = rawText ? JSON.parse(rawText) : {};
        } catch (parseError) {
          throw new Error("Backend returned invalid JSON: " + rawText);
        }

        if (!response.ok) {
          throw new Error(data.error || `Request failed with status ${response.status}`);
        }

        if (data.error) {
          throw new Error(data.error);
        }

        renderMarkdown(data.report);

        if (topicOutput) {
          topicOutput.textContent = data.topic || topic;
        }

        console.log("Parsed response data:", data);
        console.log("Report field:", data.report);
        console.log("Raw field:", data.raw);
      } catch (error) {
        showError(error.message || "Something went wrong while running the agent.");

        if (reportContent) {
          reportContent.innerHTML = "<p>No report generated.</p>";
        }
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = "Run Agent";
          submitBtn.classList.remove("loading");
        }
      }
    });
  }

  if (copyBtn && reportContent) {
    copyBtn.addEventListener("click", async function () {
      try {
        await navigator.clipboard.writeText(reportContent.innerText);
        const originalText = copyBtn.textContent;
        copyBtn.textContent = "Copied";
        setTimeout(() => {
          copyBtn.textContent = originalText;
        }, 1500);
      } catch (error) {
        alert("Could not copy the report.");
      }
    });
  }
});