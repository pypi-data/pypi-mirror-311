import feffery_antd_components as fac


def render():
    """子页面：首页渲染简单示例"""

    return fac.AntdAlert(
        type="info",
        showIcon=True,
        message="欢迎来到首页！",
        description="这里以首页为例，演示核心页面下，各子页面构建方式的简单示例😉~",
    )
