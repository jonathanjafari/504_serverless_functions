# azure/function_app.py
import json
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def _parse_hba1c(req: func.HttpRequest):
    val = req.params.get("hba1c")
    if not val:
        try:
            body = req.get_json()
            if isinstance(body, dict):
                val = body.get("hba1c")
        except ValueError:
            val = None
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

@app.route(route="hba1c", methods=["GET","POST"])
def hba1c(req: func.HttpRequest) -> func.HttpResponse:
    try:
        val = _parse_hba1c(req)
        if val is None:
            return func.HttpResponse(
                json.dumps({"error": "Provide 'hba1c' as number in query or JSON."}),
                status_code=400,
                mimetype="application/json"
            )
        result = _classify(val)
        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
            },
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": f"Unhandled error: {str(e)}"}),
            status_code=500,
            mimetype="application/json",
        )
