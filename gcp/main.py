# gcp/main.py
import json
import functions_framework

def _parse_from_request(request):
    args = request.args or {}
    if "hba1c" in args:
        val = args.get("hba1c")
    else:
        body = request.get_json(silent=True) or {}
        val = body.get("hba1c")
    try:
        return float(val) if val is not None else None
    except (TypeError, ValueError):
        return None

def _classify(hba1c: float):
    if hba1c < 5.7:
        status = "normal"
        category = "Normal (<5.7%)"
    elif 5.7 <= hba1c <= 6.4:
        status = "prediabetes"
        category = "Prediabetes (5.7–6.4%)"
    else:
        status = "diabetes"
        category = "Diabetes (≥6.5%)"
    return {"hba1c": hba1c, "status": status, "category": category}

@functions_framework.http
def hba1c(request):
    try:
        val = _parse_from_request(request)
        if val is None:
            return (json.dumps({"error": "Provide 'hba1c' as number in query or JSON."}),
                    400, {"Content-Type": "application/json",
                          "Access-Control-Allow-Origin": "*"})
        result = _classify(val)
        return (json.dumps(result), 200,
                {"Content-Type": "application/json",
                 "Access-Control-Allow-Origin": "*"})
    except Exception as e:
        return (json.dumps({"error": f"Unhandled error: {str(e)}"}), 500,
                {"Content-Type": "application/json"})
