import select
import uuid
from fastapi import APIRouter, Form
from starlette.requests import Request
from starlette.responses import RedirectResponse

from core.exception import AlertException
from core.database import db_session
from core.template import UserTemplates

from .. import plugin_config
from ..plugin_config import router_prefix, module_name

from lib.point import insert_point
from lib.common import Member, select

router = APIRouter()
templates = UserTemplates()


@router.get("/point_gift")
async def point_gift(request: Request):
    if not request.state.login_member:
        raise AlertException(detail = "로그인 후 이용해주세요.", status_code=401, url="/")
    
    return templates.TemplateResponse(
        f"{plugin_config.TEMPLATE_PATH}/user.html",
        {
            "request": request,
            "title": "포인트 선물!",
            "point": request.state.login_member.mb_point,
            "action_url": "point_gift/",
        })

@router.post("/point_gift")
async def point_gift(
    request: Request,
    db: db_session,
    receiver_id: str = Form(...),
    point: int= Form(...)
):
    """포인트 선물"""
    sender_id = request.state.login_member.mb_id
    current_point = request.state.login_member.mb_point
    
    # 포인트를 받을 회원이 존재하는지 확인
    is_exists = db.scalar(
        select(Member).where(
            Member.mb_id == receiver_id,
        )
    )
    
    if not is_exists:
        raise AlertException(detail = "포인트를 받을 회원을 찾을 수 없습니다.", status_code=404, url="point_gift")
    if sender_id == receiver_id:
        raise AlertException(detail = "자기 자신에게 포인트를 선물할 수 없습니다.", status_code=400, url="point_gift")
    if current_point < point:
        raise AlertException(detail = "포인트가 부족합니다.", status_code=400, url="point_gift")
    
    randId = str(uuid.uuid4())
    
    # 자신의 포인트 차감
    insert_point(
        request = request,
        mb_id = sender_id,
        point = -point,
        content = receiver_id + "님에게 포인트 선물 보냄",
        rel_table = "@gift",
        rel_id = "send",
        rel_action = randId,
    )
    
    # 상대방의 포인트 증가
    insert_point(
        request = request,
        mb_id = receiver_id,
        point =  point,
        content = sender_id + "님에게 포인트 선물 받음",
        rel_table = "@gift",
        rel_id = "receive",
        rel_action = randId,
    )
    
    return RedirectResponse(url=f"{module_name}", status_code=303)