# agentic-news
The **Agentic News Pipeline** is an AI-powered automation system that:

-   Collects and processes daily news from your Gmail inbox

-   Deduplicates overlapping stories across publishers

-   Summarizes important content into concise insights

-   Prioritizes stories based on your interests

-   Alerts you to high-impact topics (via email forwarding)

-   Delivers a personalized daily digest of top headlines

It's built to reduce time spent sifting through news while surfacing relevant information that matters to your business, market exposure, or interests.

* * * * *

Installation
------------

### Prerequisites

-   Python 3.8+

-   Gmail account with API access enabled

-   OpenAI API key

### 1\. Clone the Repository

```
git clone https://github.com/yourorg/agentic-news-pipeline.git
cd agentic-news-pipeline
```

### 2\. Set Up Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```

### 4\. Configure Gmail API

-   Go to https://console.developers.google.com/

-   Enable Gmail API

-   Create OAuth 2.0 Client ID

-   Download credentials and rename them to `token.json`

-   Place `token.json` in the project root

### 5\. Set Environment Variable for OpenAI

```
export OPENAI_API_KEY=your-openai-key
```

### 6\. Create Your Config

```
cp config.json.example config.json
# Edit `config.json` as needed
```

### 7\. Run the Pipeline

```
python -m agentic_news.main
# Edit `config.json` as needed
```
