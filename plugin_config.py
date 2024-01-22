import os

# module_name 는 플러그인의 폴더 이름입니다.
module_name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
router_prefix = "bbs"
admin_router_prefix = router_prefix

TEMPLATE_PATH = f"{module_name}/templates"

# 관리자 메뉴를 설정합니다.
admin_menu = {
        f"{module_name}": [
            {
                "name": "포인트 선물",
                "url": "",
                "tag": "",
            },
            {
                "id": module_name + "1",  # 메뉴 아이디
                "name": "포인트 선물 내역",
                "url": f"{admin_router_prefix}/point_gift_history",
                "tag": "demo1",
            },
        ]
    }