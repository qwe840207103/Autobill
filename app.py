import shutil
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, Request, File, UploadFile,BackgroundTasks
from fastapi.params import Form
from paddleocr import PaddleOCR
import os
load_dotenv()

from EzBookKeeping import EzBookKeeping
from Test.JDMiaoSongKnight import JDMiaoSongKnight
from Test.Common import Common

app = FastAPI()
ez = EzBookKeeping()
ez.account_list()
ez.category_list()
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False)
async def get_form(request: Request):
    form_data = await request.form()
    return dict(form_data)
@app.post("/")
async def root(
        background_tasks: BackgroundTasks,
        image: UploadFile = File(...),
        app: str = Form(...),
):
    file_path = save_image(image)
    background_tasks.add_task(test, file_path=file_path, app=app)
    return {"code": 0}

async def test(
        file_path: str,
        app: str = Form(...),
) -> None:
    result = ocr.predict(file_path)
    for res in result:
        image = ez.upload_image(file_path).get('pictureId')
        res.save_to_img("./output")
        res.save_to_json("./output")

        orc_str = ''
        for str in res._to_json()['res']['rec_texts']:
            orc_str = orc_str + str + ' '

        if app == '京东秒送骑士' or app == '美团众包':
            jd = JDMiaoSongKnight()
            json= jd.ai(orc_str,ez,ez.account_str)
            jd.add_transactions(app,json, ez, None)
        else:
            common = Common()
            json= common.ai(res._to_json()['res']['rec_texts'], ez.expend_category_str, ez.income_category_str, ez.account_str)
            ez.add_transactions(app,json, image)

##ocr识别图片
def orc_str(file_path:str):
    result = ocr.predict(file_path)
    return result

##保存图片
def save_image(image: UploadFile = File(...)):
    uuid = str(uuid4())[:8]
    file_path = os.path.join('./input/', uuid+'.png')
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return file_path

