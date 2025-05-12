# Marketing Insight Bot (GCP Cloud Run)

This project is a Flask web app that generates marketing insights using Google Gemini API based on historical Excel data and background info.

## How to Deploy

1. Create a GCP Project.
2. Enable Cloud Run, Cloud Build APIs.
3. Run:
    gcloud run deploy marketing-insight-bot --source . --region us-central1 --allow-unauthenticated
4. Send POST requests to `/ask` endpoint with:
```json
{ "prompt": "Suggest marketing strategies for X" }
