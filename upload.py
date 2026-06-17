import os
import shutil
import uuid

from typing import List

from fastapi import (
    APIRouter,
    UploadFile,
    HTTPException,
    File
)

from langchain_core.documents import Document

from app.services.document_parser import extract_text
from app.services.text_cleaner import clean_text
from app.services.chunking import chunk_text
from app.services.vector_store import get_vector_store

router = APIRouter()

UPLOAD_DIR = "app/data/uploads"
PROCESSED_DIR = "app/data/processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# =========================
# SETTINGS
# =========================

MAX_FILES = 6

MAX_FILE_SIZE = 150 * 1024 * 1024

ALLOWED_EXTENSIONS = (
    ".pdf",
    ".docx",
    ".txt",
    ".png",
    ".jpg",
    ".jpeg"
)


@router.post(
    "/upload-files",
    summary="Upload study files"
)
async def upload_files(
    files: List[UploadFile] = File(...)
):

    # =========================
    # FILE LIMIT CHECK
    # =========================

    if len(files) > MAX_FILES:

        raise HTTPException(
            status_code=400,
            detail=f"Maximum {MAX_FILES} files allowed"
        )

    results = []

    # =========================
    # PROCESS FILES
    # =========================

    for file in files:

        file_ext = os.path.splitext(
            file.filename
        )[1].lower()

        # =========================
        # VALIDATE FILE TYPE
        # =========================

        if file_ext not in ALLOWED_EXTENSIONS:

            results.append({
                "filename": file.filename,
                "status": "failed",
                "reason": "Unsupported file type"
            })

            continue

        # =========================
        # VALIDATE FILE SIZE
        # =========================

        file.file.seek(0, os.SEEK_END)

        file_size = file.file.tell()

        file.file.seek(0)

        if file_size > MAX_FILE_SIZE:

            results.append({
                "filename": file.filename,
                "status": "failed",
                "reason": "File exceeds 150MB limit"
            })

            continue

        # =========================
        # UNIQUE FILE NAME
        # =========================

        unique_name = (
            f"{uuid.uuid4()}_{file.filename}"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            unique_name
        )

        # =========================
        # SAVE FILE
        # =========================

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        try:

            # =========================
            # EXTRACT TEXT
            # =========================

            raw_text = extract_text(file_path)

            # =========================
            # CLEAN TEXT
            # =========================

            cleaned_text = clean_text(raw_text)

            # =========================
            # SAVE CLEANED TEXT
            # =========================

            processed_file = os.path.join(
                PROCESSED_DIR,
                f"{unique_name}.txt"
            )

            with open(
                processed_file,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(cleaned_text)

            # =========================
            # CHUNK TEXT
            # =========================

            chunks = chunk_text(cleaned_text)

            # =========================
            # CREATE DOCUMENTS
            # =========================

            documents = []

            for chunk in chunks:

                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "source": file.filename
                        }
                    )
                )

            # =========================
            # STORE EMBEDDINGS
            # =========================

            vectordb = get_vector_store()

            vectordb.add_documents(documents)

            # =========================
            # SUCCESS RESPONSE
            # =========================

            results.append({
                "filename": file.filename,
                "status": "success",
                "characters": len(cleaned_text),
                "chunks_created": len(chunks)
            })

        except Exception as e:

            results.append({
                "filename": file.filename,
                "status": "failed",
                "reason": str(e)
            })

    return {
        "total_files": len(files),
        "results": results
    }

@router.post("/clear-session")
async def clear_session():
    for f in os.listdir(UPLOAD_DIR):
        try:
            os.remove(os.path.join(UPLOAD_DIR, f))
        except: pass
    for f in os.listdir(PROCESSED_DIR):
        try:
            os.remove(os.path.join(PROCESSED_DIR, f))
        except: pass
    try:
        vectordb = get_vector_store()
        vectordb.delete_collection()
    except Exception:
        pass
    return {"status": "cleared"}