import time
import dash
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State, ClientsideFunction

from server import app
from views.status_pages import _404
from views.core_pages import index

# 路由配置参数
from configs import RouterConfig

app.clientside_callback(
    # 控制核心页面侧边栏折叠
    ClientsideFunction(
        namespace="clientside_basic", function_name="handleSideCollapse"
    ),
    [
        Output("core-side-menu-collapse-button-icon", "icon"),
        Output("core-header-side", "style"),
        Output("core-header-title", "style"),
        Output("core-side-menu-affix", "style"),
        Output("core-side-menu", "inlineCollapsed"),
    ],
    Input("core-side-menu-collapse-button", "nClicks"),
    [
        State("core-side-menu-collapse-button-icon", "icon"),
        State("core-header-side", "style"),
        State("core-page-config", "data"),
    ],
    prevent_initial_call=True,
)

app.clientside_callback(
    # 控制页首页面搜索切换功能
    ClientsideFunction(
        namespace="clientside_basic", function_name="handleCorePageSearch"
    ),
    Input("core-page-search", "value"),
)

app.clientside_callback(
    # 控制ctrl+k快捷键聚焦页面搜索框
    ClientsideFunction(
        namespace="clientside_basic", function_name="handleCorePageSearchFocus"
    ),
    # 其中更新key用于强制刷新状态
    [
        Output("core-page-search", "autoFocus"),
        Output("core-page-search", "key"),
    ],
    Input("core-ctrl-k-key-press", "pressedCounts"),
    prevent_initial_call=True,
)


@app.callback(
    [
        Output("core-container", "children"),
        Output("core-side-menu", "currentKey"),
        Output("core-side-menu", "openKeys"),
    ],
    Input("core-url", "pathname"),
)
def core_router(pathname):
    """核心页面路由控制及侧边菜单同步"""

    # 统一首页pathname
    if pathname == RouterConfig.index_pathname:
        pathname = "/"

    # 若当前目标pathname不合法
    if pathname not in RouterConfig.valid_pathnames.keys():
        return _404.render(), pathname, dash.no_update

    # 增加一点加载动画延迟^_^
    time.sleep(0.5)

    # 初始化页面返回内容
    page_content = fac.AntdAlert(
        type="warning",
        showIcon=True,
        message=f"这里是{pathname}",
        description="该页面尚未进行开发哦🤔~",
    )

    # 以首页做简单示例
    if pathname == "/":
        # 更新页面返回内容
        page_content = index.render()

    return [
        page_content,
        pathname,
        RouterConfig.side_menu_open_keys.get(pathname, dash.no_update),
    ]
