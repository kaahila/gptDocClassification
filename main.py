from fastapi import FastAPI, UploadFile, HTTPException
from io import BytesIO, StringIO
from PIL import Image
import uvicorn

from database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/image/")
async def upload_image(file: UploadFile):
    if file.content_type != 'image/jpeg':
        raise HTTPException(status_code=422, detail="file type not accepted")
    request_object_content = await file.read()
    try:
        img = Image.open(BytesIO(request_object_content))
        img = img.resize((500, 750))
        buffer = StringIO()
        img.save('./img.jpg', "JPEG", quality=80)
    except Exception as e:
        raise HTTPException(status_code=400, detail="image not processable")
    return {"filename": file.filename}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
