# AI-Powered Cloud Cost Optimizer

A Python-based CLI tool that uses LLMs (via Hugging Face) to analyze project descriptions, generate synthetic billing data, and provide cloud cost optimization recommendations.

## Features

*   **Project Profile Generation**: Converts natural language project descriptions into structured technical profiles (JSON).
*   **Synthetic Billing Generation**: Creates realistic monthly billing data based on the project profile.
*   **Cost Analysis & Reporting**: Analyzes the billing data against the budget and generates actionable optimization recommendations (Right-sizing, Free Tier, Open Source).
*   **Interactive CLI**: Simple menu-driven interface.

## Prerequisites

*   Python 3.8 or higher
*   A Hugging Face Account and Access Token (Read permissions)

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository-url>
    cd cloud-cost-optimizer
    ```

2.  **Create and Activate a Virtual Environment**:
    *   **Windows**:
        ```bash
        python -m venv venv
        .\venv\Scripts\Activate
        ```
    *   **macOS/Linux**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Create a `.env` file in the root directory.
2.  Add your Hugging Face token to the file:
    ```env
    HF_TOKEN=your_hugging_face_token_here
    ```

## Usage

Run the main application script:

```bash
python main.py
```

### Workflow

1.  **Enter New Project Description** (Option 1):
    *   Enter a description of your project (e.g., "A food delivery app for 10k users...").
    *   Press Enter to use the default example if you like.
    *   This saves to `project_description.txt`.

2.  **Run Complete Cost Analysis** (Option 2):
    *   Reads the description.
    *   Generates `project_profile.json` (Architecture & Requirements).
    *   Generates `mock_billing.json` (Synthetic monthly cloud bill).
    *   Generates `cost_optimization_report.json` (Analysis & Savings).

3.  **View Recommendations** (Option 3):
    *   Displays the summary of the report.
    *   Shows total costs, budget variance, and top cost-saving recommendations.

## Project Structure

*   `main.py`: The entry point and CLI interface.
*   `backend.py`: Contains logic for LLM interaction, JSON parsing, and file handling.
*   `requirements.txt`: Python package dependencies.
*   `.env`: Configuration file for API keys (not committed to version control).
*   `*.json`: Generated data files (Profile, Billing, Report).

## Troubleshooting

*   **Unicode Errors (Windows)**: The application has been patched to use UTF-8 encoding for stdout and avoids non-ASCII characters in the console to prevent crashes on standard Windows terminals.
*   **API Errors**: If the analysis fails, ensure your `HF_TOKEN` is valid and has permissions to access the `meta-llama/Llama-3.1-8B-Instruct` model.

## Credits

Uses [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) via Hugging Face Inference API.
