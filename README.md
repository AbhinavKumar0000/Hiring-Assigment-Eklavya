# AI Assessment Generator

A full-stack AI application that generates educational content (explanations + MCQs) for substantial grades and topics, validates it using a secondary AI reviewer, and automatically refines it if necessary.

## Project Overview

This tool uses a multi-agent system architecture to ensure high-quality educational content:
1.  **Generator Agent**: Creates content based on Grade and Topic.
2.  **Reviewer Agent**: Evaluates the content for age appropriateness, correctness, and clarity.
3.  **Refinement Pipeline**: If the Reviewer rejects the content, the Generator is triggered again with specific feedback to improve the output (single pass).

## Tech Stack
-   **Backend**: Python, FastAPI
-   **Frontend**: HTML, CSS, Vanilla JavaScript
-   **AI Model**: Google Gemini 2.0 Flash (via `google-generativeai`)
-   **Architecture**: Stateless Agentic Pipeline

## Architecture & Agent Logic

### 1. Generator Agent (`backend/generator.py`)
-   **Input**: Grade (int), Topic (str)
-   **Output**: JSON object containing an `explanation` and 3 `mcqs`.
-   **Refinement**: Can accept `feedback` to adjust its output in a second pass.

### 2. Reviewer Agent (`backend/reviewer.py`)
-   **Input**: The output from the Generator.
-   **Logic**: Checks for factual accuracy and grade-level appropriateness.
-   **Output**: Pass/Fail status with specific feedback strings.

### 3. Pipeline (`backend/pipeline.py`)
-   Orchestrates the sequential flow:
    `User Request -> Generator -> Reviewer -> (If Fail: Generator Refinement) -> Response`

## Setup Instructions

### Prerequisites
-   Python 3.9 or higher
-   A Google Gemini API Key

### Installation

1.  **Clone the repository** (or navigate to the project folder).
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure API Key**:
    -   Rename `.env.example` to `.env`.
    -   Add your Gemin API Key:
        ```
        GEMINI_API_KEY=your_actual_api_key_here
        ```

## Running the Application

1.  **Start the Server**:
    ```bash
    python -m backend.main
    ```
2.  **Open in Browser**:
    Visit `http://localhost:8000`

    *Note: The frontend is now served directly by the backend, so you don't need a separate frontend server.*

## Example Usage

**Request**:
-   **Grade**: 5
-   **Topic**: "The Water Cycle"

**Flow**:
1.  **Generator** produces an explanation of Evaporation, Condensation, Precipitation and 3 MCQs.
2.  **Reviewer** checks the content.
    -   *Scenario A (Pass)*: Output is returned immediately.
    -   *Scenario B (Fail)*: Reviewer notes "Language too complex for Grade 5". Pipeline calls Generator again with this feedback. Generator simplifies text. Refined output is returned.

## API Reference

### `POST /generate`

**Request Body**:
```json
{
  "grade": 5,
  "topic": "Photosynthesis"
}
```

**Response**:
```json
{
  "initial_output": { ... },
  "review_output": {
    "status": "fail",
    "feedback": ["Explanation is too complex."]
  },
  "refined_output": { ... } // Only present if status was fail
}
```
