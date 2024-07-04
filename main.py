from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functions.active_infos import get_infos
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ActivesRequest(BaseModel):
    actives_list: List[str]


@app.post("/actives-infos")
async def actives_infos(actives: ActivesRequest):
    infos = get_infos(actives.actives_list)
    return infos


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5680)
