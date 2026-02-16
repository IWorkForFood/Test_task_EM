from fastapi import APIRouter, Depends
from sqlalchemy import select 
from app.database import async_session_maker 
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from .models import TextReport
from .shemas import STextReport, STextReportUpdate
from sqlalchemy import text, insert
from .dao import TextReportsDAO
import uuid
import datetime
import os

router_textreports = APIRouter(prefix='/textroports', tags=['Работа с отчетами'])

@router_textreports.post("/new_textreport", response_model=STextReport)
async def upload_files(upload_file: UploadFile, filename: str):

    unique_dirname = f"{datetime.datetime.now()}/{uuid.uuid4()}"
    
    directory = f"./textreport/{unique_dirname}"  
    os.makedirs(directory, exist_ok = True)

    file = upload_file.file
    suffix = upload_file.filename.split('.')[-1]
    filename = '.'.join([filename, suffix])
    directory_with_file = os.path.join(directory, filename)

    with open(directory_with_file, "wb") as f:
        f.write(file.read())

    new_textreport = await TextReportsDAO.add(filename=filename, path=directory_with_file)

    response = {'filename': filename, 'path': directory_with_file}

    return response

@router_textreports.post("/find_all_textreports")
async def find_all_textreports_data() -> list[STextReport]:
    return await TextReportsDAO.find_all()

@router_textreports.get("/find_one_or_none", summary="Получить один отчет по фильтру")
async def find_one_or_none(file_id: int) -> STextReport:
    textreport = await TextReportsDAO.find_one_or_none(id = file_id)
    return textreport

@router_textreports.get("/download")
async def download_file(file_id: int):
    textreport = await TextReportsDAO.find_one_or_none(id = file_id)
    absolute_path = os.path.abspath(textreport.path)
    return FileResponse(path=f"{absolute_path}", filename=f"{os.path.basename(absolute_path)}", media_type="application/octet-stream")


@router_textreports.patch("/patch_textreport/{file_id}")
async def update_textreport(file_id: int, update: STextReportUpdate = Depends(), upload_file: UploadFile = None):

    update_dict = update.model_dump(exclude_unset=True)
    textreport = await TextReportsDAO.find_one_or_none(id = file_id)
    path_with_file = textreport.path
    original_path = os.path.dirname(path_with_file)

    os.remove(path_with_file)
    suffix = upload_file.filename.split('.')[-1]
    filename = '.'.join([update.filename, suffix])
    new_textreport_path = os.path.join(original_path, filename)
    absolute_path = os.path.abspath(new_textreport_path)
    file = upload_file.file

    with open(new_textreport_path, "wb") as f:
        f.write(file.read())

    update_dict['path'] = new_textreport_path

    if not update_dict:
        raise HTTPException(400, "No valid fields to update")

    result = await TextReportsDAO.update({'id': file_id}, **update_dict)
    return update

@router_textreports.delete("/delete_textreport/{file_id}")
async def update_textreport(file_id: int):

    check = await TextReportsDAO.delete_student_by_id(file_id)
    if check:
        return {"message": "Файл был успешно удален."}
    else:
        return {"message": "Не удалось удалить файл."}







