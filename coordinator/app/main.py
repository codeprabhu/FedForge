from fastapi import FastAPI # type: ignore
app = FastAPI(
    title = "FedForge Coordinator",
    version = "0.1.0"
)

@app.get("/")
async def root():
    return {
        "service" : "fedforge-coordinator",
        "status" : "online",
        "version" : "0.1.0"
    }