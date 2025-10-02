# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# import json
# import numpy as np
# import os

# app = FastAPI()

# # ✅ Enable CORS globally
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],       # allow any origin
#     allow_methods=["*"],       # POST, GET, OPTIONS etc.
#     allow_headers=["*"],       # allow all headers
# )

# # Helper to load telemetry bundle
# def load_telemetry():
#     data_path = os.path.join(os.path.dirname(__file__), "q-vercel-latency.json")
#     with open(data_path, "r") as f:
#         return json.load(f)

# @app.options("/metrics")
# async def options_metrics():
#     return JSONResponse(
#         content={},
#         headers={
#             "Access-Control-Allow-Origin": "*",
#             "Access-Control-Allow-Methods": "POST, OPTIONS",
#             "Access-Control-Allow-Headers": "*",
#         },
#     )




# # ✅ POST endpoint
# @app.post("/metrics")
# async def metrics(request: Request):
#     body = await request.json()
#     regions = body.get("regions", [])
#     threshold = body.get("threshold_ms", 180)
#     data = load_telemetry()
#     result = {}

#     for region in regions:
#         region_data = [d for d in data if d["region"] == region]
#         if not region_data:
#             result[region] = {
#                 "avg_latency": None,
#                 "p95_latency": None,
#                 "avg_uptime": None,
#                 "breaches": 0
#             }
#             continue

#         latencies = [d["latency_ms"] for d in region_data]
#         uptimes = [d["uptime_pct"] for d in region_data]
#         breaches = sum(1 for d in region_data if d["latency_ms"] > threshold)

#         result[region] = {
#             "avg_latency": float(np.mean(latencies)),
#             "p95_latency": float(np.percentile(latencies, 95)),
#             "avg_uptime": float(np.mean(uptimes)),
#             "breaches": breaches
#         }

#     # ✅ Explicitly include CORS headers in response
#     return JSONResponse(
#         content=result,
#         headers={
#             "Access-Control-Allow-Origin": "*",
#             "Access-Control-Allow-Methods": "POST, OPTIONS",
#             "Access-Control-Allow-Headers": "*",
#         },
#     )



from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from pathlib import Path

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Load the dataset once when the app starts
# The data file should be in the same directory as this script
DATA_FILE = Path(__file__).parent / "q-vercel-latency.json"
df = pd.read_json(DATA_FILE)


@app.get("/")
async def root():
    return {"message": "Vercel Latency Analytics API is running."}


@app.post("/api/")
async def get_latency_stats(request: Request):
    payload = await request.json()
    regions_to_process = payload.get("regions", [])
    threshold = payload.get("threshold_ms", 200)

    results = []

    for region in regions_to_process:
        region_df = df[df["region"] == region]

        if not region_df.empty:
            avg_latency = round(region_df["latency_ms"].mean(), 2)
            p95_latency = round(np.percentile(region_df["latency_ms"], 95), 2)
            avg_uptime = round(region_df["uptime_pct"].mean(), 3)
            breaches = int(region_df[region_df["latency_ms"] > threshold].shape[0])

            results.append(
                {
                    "region": region,
                    "avg_latency": avg_latency,
                    "p95_latency": p95_latency,
                    "avg_uptime": avg_uptime,
                    "breaches": breaches,
                }
            )

    return {"regions": results}

