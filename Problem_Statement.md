# EDGE MINDS HACKATHON 2026

#### Team : Electro_Neurons (ID : EDGM26-DWDPMR)

**Project Title** :
Autonomous Local Research Agent Using LLaMA 3.2 (1B)

**Introduction**

Research tasks often require more than a single prompt. A useful research system must break a topic into smaller questions, search for relevant information, filter useful evidence, summarize findings, and compile them into a structured final report.

This project implements an autonomous local research agent powered by the LLaMA 3.2 (1B parameter) Small Language Model, deployed on the NVIDIA Jetson Orin Nano. The model acts as the central reasoning engine, planning sub-questions, searching local text files, generating evidence-backed summaries, and producing a final report without intermediate user guidance.

This approach ensures low-latency offline operation, improved auditability, and strong privacy, making it suitable for environments where external APIs cannot be used.

**Objectives**

    Design a lightweight AI research assistant using LLaMA 3.2 (1B) as the core reasoning model.

    Enable the system to autonomously generate sub-questions and decide execution flow (agentic behavior).

    Implement local document search over a folder of text files without internet dependency.

    Extract and summarize relevant evidence for each sub-question.

    Compile structured, coherent final reports from intermediate summaries.

    Optimize the system for efficient deployment on Jetson Orin Nano.

**Methodology**

    The system follows a multi-stage agentic pipeline driven by LLaMA 3.2 (1B):

    User Input
    The user provides a research topic.

    Planning (SLM - LLaMA 3.2)
    The model generates 3–6 sub-questions and determines the order of execution.

    Local Retrieval Tool
    A file search module scans local text documents, extracts relevant snippets, and returns file references.

    Reasoning + Summarization (SLM)
    LLaMA 3.2 processes retrieved content to generate concise, evidence-based answers for each sub-question.

    Iterative Agent Loop
    The model evaluates coverage and decides whether additional sub-questions are needed.

    Report Compilation
    All summaries are merged into a structured final research report.

    The architecture is optimized for edge deployment, ensuring low memory footprint and efficient inference using the 1B parameter model.

**Scope**

    Offline academic research assistant

    Local knowledge base querying system

    Privacy-sensitive environments (defense, healthcare, enterprise)

    Edge AI deployment on Jetson devices

**Future improvements may include:**

    Document chunking and embedding-based retrieval

    Vector search integration

    Confidence scoring for retrieved evidence

    Persistent memory and improved agent state tracking

    Fine-tuning or prompt optimization specific to LLaMA 3.2 (1B)
