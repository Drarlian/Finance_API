from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
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


@app.post("/actives-infos/{type_active}")
async def actives_infos(actives: ActivesRequest, type_active: str):
    if type_active in ['acoes', 'fiis']:
        infos = get_infos(actives.actives_list, type_active)

        if infos is not None:
            return JSONResponse(status_code=200, content=infos)
        else:
            return JSONResponse(status_code=404, content={"message": "Ativo não encontrado"})
    else:
        return JSONResponse(status_code=404, content={"message": "Type Active Invalid"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5680)
