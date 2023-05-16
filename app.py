from uuid import uuid4

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from starlette.responses import FileResponse

from db import create_user, save_audio, check_user_credentials, check_audio_record_exists, get_user_by_name
from from_wav_to_mp3 import convert_to_mp3
from models_serializer import CreateUserRequest

app = FastAPI()


@app.post("/users")
def create_user_route(request: CreateUserRequest) -> dict:
    """
    Creating a user
    :param request:
    :return:
    """
    existing_user = get_user_by_name(request.name)
    if existing_user:
        return {"message": "User already exists"}

    user = create_user(request.name)
    return {"id": user.id, "access_token": user.access_token}


@app.post("/record")
def create_audio_record(user_id: int = Form(...), access_token: str = Form(...), file: UploadFile = File(...)) -> dict:
    """
    creating an audio record
    :param user_id:
    :param access_token:
    :param file:
    :return url link to download file as mp3:
    """
    if not check_user_credentials(user_id, access_token):
        raise HTTPException(status_code=401, detail="Invalid user credentials")

    mp3_audio = convert_to_mp3(file.file)
    audio_id = str(uuid4())

    mp3_audio_path = f"./audio/{audio_id}.mp3"
    with open(mp3_audio_path, "wb") as buffer:
        buffer.write(mp3_audio.getbuffer())

    record = save_audio(user_id, audio_id)

    return {"id": record.id, "url": f"http://127.0.0.1:8000/record?id={audio_id}&user={user_id}"}


@app.get("/record")
def download_audio_record(id: str, user: int) -> FileResponse:
    """
    :param id_:
    :param user:
    :return link to download audio file as mp3 if exists:
    """
    if not check_audio_record_exists(id, user):
        raise HTTPException(status_code=404, detail="Audio record not found")
    audio_path = f"./audio/{id}.mp3"

    return FileResponse(audio_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
