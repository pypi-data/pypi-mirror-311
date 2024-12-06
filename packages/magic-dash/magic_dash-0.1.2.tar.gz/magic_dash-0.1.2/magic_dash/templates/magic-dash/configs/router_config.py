from typing import List


class RouterConfig:
    """路由配置参数"""

    # 与应用首页对应的pathname地址
    index_pathname: str = "/index"

    # 核心页面侧边菜单结构
    core_side_menu: List[dict] = [
        {
            "component": "ItemGroup",
            "props": {
                "title": "主要页面",
                "key": "主要页面",
            },
            "children": [
                {
                    "component": "Item",
                    "props": {
                        "title": "首页",
                        "key": "/",
                        "icon": "antd-home",
                        "href": "/",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "示例页面1",
                        "key": "/core/page1",
                        "icon": "antd-app-store",
                        "href": "/core/page1",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "示例页面2",
                        "key": "/core/page2",
                        "icon": "antd-app-store",
                        "href": "/core/page2",
                    },
                },
                {
                    "component": "SubMenu",
                    "props": {
                        "key": "示例页面3",
                        "title": "示例页面3",
                        "icon": "antd-catalog",
                    },
                    "children": [
                        {
                            "component": "Item",
                            "props": {
                                "key": "/core/page3-1",
                                "title": "示例页面3-1",
                                "href": "/core/page3-1",
                            },
                        },
                        {
                            "component": "Item",
                            "props": {
                                "key": "/core/page3-2",
                                "title": "示例页面3-2",
                                "href": "/core/page3-2",
                            },
                        },
                        {
                            "component": "Item",
                            "props": {
                                "key": "/core/page3-3",
                                "title": "示例页面3-3",
                                "href": "/core/page3-3",
                            },
                        },
                    ],
                },
            ],
        },
        {
            "component": "ItemGroup",
            "props": {
                "title": "其他页面",
                "key": "其他页面",
            },
            "children": [
                {
                    "component": "Item",
                    "props": {
                        "title": "示例页面4",
                        "key": "/core/page4",
                        "icon": "antd-app-store",
                        "href": "/core/page4",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "示例页面5",
                        "key": "/core/page5",
                        "icon": "antd-app-store",
                        "href": "/core/page5",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "示例页面6",
                        "key": "/core/page6",
                        "icon": "antd-app-store",
                        "href": "/core/page6",
                    },
                },
            ],
        },
    ]

    # 有效页面pathname地址 -> 页面标题映射字典
    valid_pathnames: dict = {
        "/": "首页",
        index_pathname: "首页",
        "/core/page1": "示例页面1",
        "/core/page2": "示例页面2",
        "/core/page3-1": "示例页面3-1",
        "/core/page3-2": "示例页面3-2",
        "/core/page3-3": "示例页面3-3",
        "/core/page4": "示例页面4",
        "/core/page5": "示例页面5",
        "/core/page6": "示例页面6",
        "/404-demo": "404状态页演示",
        "/500-demo": "500状态页演示",
    }

    # 部分页面pathname对应要展开的子菜单层级
    side_menu_open_keys: dict = {
        "/core/page3-1": ["示例页面3"],
        "/core/page3-2": ["示例页面3"],
        "/core/page3-3": ["示例页面3"],
    }
