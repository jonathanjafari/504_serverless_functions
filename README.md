# 504_serverless_functions

**Video walkthrough:** <PASTE LOOM/ZOOM LINK HERE>

This repo mirrors a classmate-style layout and implements a simple **HbA1c** rule as the lab value (not blood pressure).

---

## Cloud Environments Used and Regions
- **Azure Functions (HTTP trigger)** — Region: `eastus` (example)
- **Google Cloud Functions Gen2** — Region: `us-central1` (example)

---

## Public Endpoint URLs (paste after you deploy)
- **Azure:** `https://<your-funcapp>.azurewebsites.net/api/hba1c?code=<FUNCTION_KEY>`
- **GCP:** `https://<your-cloud-function-url>`

---

## Example Requests

### GET (Azure with function key)
```bash
curl "https://<your-funcapp>.azurewebsites.net/api/hba1c?hba1c=6.1&code=<FUNCTION_KEY>"
```

### GET (GCP, public for demo)
```bash
curl "https://<your-cloud-function-url>?hba1c=6.1"
```

### POST (recommended for demo video)
```python
import requests

payloads = [{"hba1c": 5.6}, {"hba1c": 6.1}, {"hba1c": 6.7}]
print("Azure:")
for p in payloads:
    print(requests.post("https://<your-funcapp>.azurewebsites.net/api/hba1c?code=<FUNCTION_KEY>", json=p, timeout=10).json())

print("GCP:")
for p in payloads:
    print(requests.post("https://<your-cloud-function-url>", json=p, timeout=10).json())
```

**Expected behavior:**
- `5.6` → `"status": "normal"`, `"category": "Normal (<5.7%)"`
- `6.1` → `"status": "prediabetes"`, `"category": "Prediabetes (5.7–6.4%)"`
- `6.7` → `"status": "diabetes"`, `"category": "Diabetes (≥6.5%)"`

---

## HbA1c Rule (Lab Rule)
- **Normal:** HbA1c `< 5.7%`
- **Prediabetes:** `5.7–6.4%`
- **Diabetes:** `≥ 6.5%`
- Based on ADA diagnostic cut points.

> You will demo a *lab value* (HbA1c). Do **not** use blood pressure as your chosen lab.

---

## Deployment — Step by Step (Beginner Friendly)

### 1) Prepare your machine
- Install **Git**, **Python 3.11+**, **pip**.
- Install CLIs:
  - **Azure CLI:** https://learn.microsoft.com/cli/azure/install-azure-cli
  - **Azure Functions Core Tools v4:** https://learn.microsoft.com/azure/azure-functions/functions-run-local
  - **Google Cloud SDK:** https://cloud.google.com/sdk/docs/install

### 2) Get this repo into a folder
```bash
# Unzip the starter zip you downloaded
unzip 504_serverless_functions_starter.zip -d ~/code
cd ~/code/504_serverless_functions
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Deploy to **Azure Functions**
```bash
az login
az group create -n rg-504 -l eastus
az storage account create -n <storageNameUniq> -g rg-504 -l eastus --sku Standard_LRS

az functionapp create   -g rg-504   -n <funcapp-uniq>   -s <storageNameUniq>   -c eastus   --consumption-plan-location eastus   --runtime python   --runtime-version 3.11   --os-type linux

# Publish (from repo root)
cd azure
func azure functionapp publish <funcapp-uniq>

# Get the function URL with code in Azure Portal:
# Function App → Functions → hba1c → "Get Function URL"
```

### 4) Deploy to **Google Cloud Functions (Gen2)**
```bash
gcloud auth login
gcloud config set project <YOUR_PROJECT_ID>
cd gcp
gcloud functions deploy hba1c   --gen2   --runtime=python312   --region=us-central1   --source=.   --entry-point=hba1c   --trigger-http   --allow-unauthenticated

# Copy the URL shown after deploy.
```

### 5) Test
Use the curl/python examples above. Confirm you get JSON back.

### 6) Screenshots
Save screenshots into `images/`:
- Azure URL in browser, example result JSON, logs/monitor, terminal publish
- GCP URL in browser, example result JSON, logs tab, terminal deploy

### 7) Record 2–4 minute video
- Show repo structure (`azure/`, `gcp/`, `images/`)
- Show both URLs
- Run one normal and one diabetes request (e.g., 5.6 and 6.7)
- Show logs in both clouds
- Mention any gotchas (function key, cold start, region)

---

## Comparison (short)
- **Azure:** Secure by default (function key). First-time setup needs storage + app; Core Tools make local/dev easy.
- **GCP:** One command deploy, public URL flag. Logs are easy in the console; Gen2 cold starts acceptable for demo.

---

## References (ADA)
- ADA “Diabetes Diagnosis & Tests” — A1C thresholds (normal <5.7%, prediabetes 5.7–6.4%, diabetes ≥6.5%).
