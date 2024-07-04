from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functions.active_infos import get_infos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/active/{active_name}")
async def get_active_infos(active_name: str):
    infos = get_infos(active_name)
    return infos


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5680)
