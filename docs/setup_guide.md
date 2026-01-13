# Setup and Installation Guide

## Prerequisites
-   Python 3.8 or higher.
-   Git.

## Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd <repo-name>
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Project
The main entry point is `main.py`. This script runs a full demonstration workflow.

```bash
python main.py
```

### What happens when you run it?
1.  Downloads SPY data from 2015 to 2024.
2.  Calculates indicators.
3.  Trains the Random Forest model on data from 2015-2021.
4.  Backtests both the MA Strategy and ML Strategy on unseen data (2022-2023).
5.  Prints performance metrics to the console.
6.  Saves a comparison chart to `strategy_comparison.png`.
