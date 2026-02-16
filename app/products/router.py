from sqlalchemy import select 
from app.database import async_session_maker 
from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Depends
from fastapi.responses import FileResponse
from .models import TextReport
from .shemas import STextReport, STextReportUpdate
from sqlalchemy import text, insert
from .dao import TextReportsDAO
from app.tasks import test_task
import datetime
import os
import time
from .dao import TextReportsDAO
from app.users.dependencies import get_current_user
from app.user_customization.dao import TypicalDataDAO
from app.users.models import User
from .utils import ReportCreator2000
import uuid

router_textreports = APIRouter(prefix='/textroports', tags=['Работа с отчетами'])

@router_textreports.post("/task")
async def task(filename: str, md_file: UploadFile, user_data: User = Depends(get_current_user)):

    dir_path = "./process_files"

    md_file_name = md_file.filename

    absolute_path = os.path.abspath(dir_path)

    uniqe_md_path = f"{user_data.id}"
    unique_dirname = f"{uniqe_md_path}/{datetime.datetime.now()}/{uuid.uuid4()}"
    absolute_uniqe_dirname = os.path.join(absolute_path, unique_dirname)
    absolute_uniqe_md_path = os.path.join(absolute_path, uniqe_md_path)
    md_path_with_filename = f"{uniqe_md_path}/{md_file_name}"
    abs_md_path_with_filename = os.path.join(absolute_path, md_path_with_filename)

    #path_exists = True
    #while path_exists:
    #    try:
    #        os.makedirs(path)
    #        break
    #    except Exception:
    #        continue
    os.makedirs(absolute_uniqe_dirname)

    
    with open(abs_md_path_with_filename, 'wb') as file:
        file.write(md_file.file.read())

    rep = ReportCreator2000(output_dir = absolute_path)
    typical_data = await TypicalDataDAO.find_one_or_none(user_id = user_data.id)
    

    title_vars = {
        "name": f'{typical_data.author_lastname} {typical_data.author_firstname[0].upper()}. {typical_data.author_surname[0].upper()}.',
        "group_number": typical_data.group_number,
        "student_id": typical_data.record_book_number,
        "supervisor": f'{typical_data.instructor_lastname} {typical_data.instructor_firstname[0].upper()}. {typical_data.instructor_surname[0].upper()}.',
        "work_title": typical_data.work_title,
        "completion_year": typical_data.completion_year,
        "department": typical_data.department,
        "institute": typical_data.institute
    }


    result = rep.create_new_report(
        content_md_path = f"{uniqe_md_path}/{md_file_name}",
        content_docx_path="content.docx",
        reference_style_docx="custom-reference2.docx",
        title_template_path="Titul.docx",
        filled_title_path="new_titul.docx",
        final_report_path=f"{unique_dirname}/{filename}.docx",
        **title_vars
    )

    await TextReportsDAO.add(filename=os.path.basename(result), path=result, user_id = user_data.id)
    
    return FileResponse(path=f"{result}", filename=f"{os.path.basename(result)}", media_type="application/octet-stream")



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
    if not textreport:
        raise HTTPException(status_code=404, detail="Отчет не найден")
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







