from flask import jsonify

def _classify(a1c: float) -> str:
    if a1c >= 6.5:
        return "diabetes"
    if a1c >= 5.7:
        return "prediabetes"
    return "normal"

def hba1c(request):
    """GET /?a1c=6.1  or POST JSON {"a1c": 6.1}"""
    value = None

    # Try JSON
    data = request.get_json(silent=True) or {}
    value = data.get("a1c", data.get("value"))

    # Fallback to query param
    if value is None and request.args:
        value = request.args.get("a1c", request.args.get("value"))

    # Validate
    try:
        a1c = float(value)
    except (TypeError, ValueError):
        return jsonify({
            "error": "Provide HbA1c as 'a1c' (or 'value') via GET ?a1c=6.1 or POST JSON {\"a1c\": 6.1}"
        }), 400

    return jsonify({"a1c": a1c, "classification": _classify(a1c)})
