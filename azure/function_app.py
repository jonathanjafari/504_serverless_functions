# azure/function_app.py
import json
import azure.functions as func

# Public demo: no key required
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def _parse_hba1c(req: func.HttpRequest):
    # Accept both names: a1c or hba1c
    val = req.params.get("a1c") or req.params.get("hba1c")
    if not val:
        try:
            body = req.get_json()
            if isinstance(body, dict):
                val = body.get("a1c") or body.get("hba1c")
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

@app.route(route="hba1c", methods=["GET","POST"], auth_level=func.AuthLevel.ANONYMOUS)
def hba1c(req: func.HttpRequest) -> func.HttpResponse:
    try:
        val = _parse_hba1c(req)
        if val is None:
            return func.HttpResponse(
                json.dumps({"error": "Provide 'a1c' (or 'hba1c') as a number in query or JSON."}),
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
