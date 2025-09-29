from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import numpy as np
import os

app = FastAPI()

# ✅ Enable CORS globally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # allow any origin
    allow_methods=["*"],       # POST, GET, OPTIONS etc.
    allow_headers=["*"],       # allow all headers
)

# Helper to load telemetry bundle
def load_telemetry():
    data_path = os.path.join(os.path.dirname(__file__), "q-vercel-latency.json")
    with open(data_path, "r") as f:
        return json.load(f)

# ✅ POST endpoint
@app.post("/metrics")
async def metrics(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 180)
    data = load_telemetry()
    result = {}

    for region in regions:
        region_data = [d for d in data if d["region"] == region]
        if not region_data:
            result[region] = {
                "avg_latency": None,
                "p95_latency": None,
                "avg_uptime": None,
                "breaches": 0
            }
            continue

        latencies = [d["latency_ms"] for d in region_data]
        uptimes = [d["uptime_pct"] for d in region_data]
        breaches = sum(1 for d in region_data if d["latency_ms"] > threshold)

        result[region] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": breaches
        }

    # ✅ Explicitly include CORS headers in response
    return JSONResponse(
        content=result,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )
