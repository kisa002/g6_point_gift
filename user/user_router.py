from fastapi import APIRouter, Form
from starlette.requests import Request
from starlette.responses import RedirectResponse

from core.template import UserTemplates
from .. import plugin_config
from ..plugin_config import module_name

from lib.point import insert_point, delete_point

router = APIRouter()

templates = UserTemplates()


@router.get("/point_gift_json")
async def show(request: Request):
    """json 출력예시"""
    return {"message": "Hello POINT GIFT JSON!"}


@router.get("/point_gift")
async def show(request: Request):
    """템플릿 출력예시"""
    return templates.TemplateResponse(
        f"{plugin_config.TEMPLATE_PATH}/user_demo.html",
        {
            "request": request,
            "title": "포인트 선물!",
            "point": request.state.login_member.mb_point,
            "action_url": "point_gift/",
            "content": f"Hello {module_name}!",
        })

@router.post("/point_gift")
async def gift_point(request: Request, receiver_id: str = Form(...), point: int= Form(...)):
    """포인트 선물"""
    # delete_point(requset, request.state.login_member.mb_id, point, request.state.login_member.mb_id + "님에게 포인트 선물", "", "", "")
    
    sender_id = request.state.login_member.mb_id
    print("sender:", sender_id, "receiver:", receiver_id, "point:", point)
    
    # 자신의 포인트 차감
    insert_point(request, receiver_id, point, sender_id + "님에게 포인트 선물 받음", "", "", "")
    
    # 상대방의 포인트 증가
    insert_point(request, sender_id, -point, receiver_id + "님에게 포인트 선물 보냄", "", "", "")
    
    return templates.TemplateResponse(
        f"{plugin_config.TEMPLATE_PATH}/user_demo.html",
        {
            "request": request,
            "title": "포인트 선물!",
            "point": request.state.login_member.mb_point,
            "action_url": "point_gift/",
            "content": f"Hello {module_name}!",
        })