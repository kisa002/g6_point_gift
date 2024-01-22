from fastapi import APIRouter
from sqlalchemy import select, or_, and_
from starlette.requests import Request
from starlette.responses import RedirectResponse

from core.plugin import get_admin_plugin_menus, get_all_plugin_module_names
from core.database import db_session
from core.template import AdminTemplates
from core.models import Member, Point

from lib.common import get_admin_menus, get_client_ip
from lib.template_functions import (
    get_editor_select, get_member_id_select, get_member_level_select,
    get_selected, get_skin_select, option_array_checked
)
from . import plugin_config
from ..plugin_config import module_name, admin_router_prefix

templates = AdminTemplates()

templates.env.globals["admin_menus"] = get_admin_menus()
templates.env.globals["getattr"] = getattr
templates.env.globals["get_member_id_select"] = get_member_id_select
templates.env.globals["get_skin_select"] = get_skin_select
templates.env.globals["get_editor_select"] = get_editor_select
templates.env.globals["get_selected"] = get_selected
templates.env.globals["get_member_level_select"] = get_member_level_select
templates.env.globals["option_array_checked"] = option_array_checked
templates.env.globals["get_admin_plugin_menus"] = get_admin_plugin_menus
templates.env.globals["get_client_ip"] = get_client_ip
templates.env.globals["get_all_plugin_module_names"] = get_all_plugin_module_names

admin_router = APIRouter(prefix=f"/{admin_router_prefix}", tags=['demo_admin'])

@admin_router.get("/point_gift_history")
async def point_gift_history(request: Request, db: db_session):
    request.session["menu_key"] = module_name
    request.session["plugin_submenu_key"] = module_name + "1"
    
    # 포인트 선물 내역 조회
    temp_gifts = db.scalars(
        select(Point).where(
            Point.po_rel_table == "@gift"
        )
    ).all()
    
    gifts = {}
    
    for gift in temp_gifts:
        actionId = str(gift.po_rel_action).strip()
        if actionId not in gifts:
            gifts[actionId] = {}
        
        if gift.po_rel_id == "send":
            gifts[actionId]["sender"] = gift.mb_id
            gifts[actionId]["point"] = gift.po_point
            gifts[actionId]["datetime"] = gift.po_datetime
        elif gift.po_rel_id == "receive":
            gifts[actionId]["receiver"] = gift.mb_id
    
    
    context = {
        "request": request,
        "title": "포인트 선물 내역",
        "content": f"Hello {module_name}",
        "gifts": gifts,
        "module_name": module_name,
    }
    return templates.TemplateResponse(f"{plugin_config.TEMPLATE_PATH}/admin/admin.html", context)