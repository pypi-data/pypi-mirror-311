import os
import click
import shutil

__version__ = "0.1.2"


@click.group(name="magic-dash")
@click.version_option(version=__version__, message="%(version)s")
def magic_dash():
    """magic-dash命令行工具"""

    pass


@click.command(name="list")
def _list():
    """列出当前可生成的全部Dash应用项目模板"""
    click.echo("内置Dash应用项目模板：\n")
    # 为magic-dash输出添加高亮颜色
    click.echo(click.style("- magic-dash    基础多页面应用模板", fg="blue"))
    click.echo(click.style("- simple-tool    单页面工具应用模板", fg="blue"))


@click.command(name="create")
@click.option("--name", required=True, type=click.STRING, help="Dash应用项目模板名称")
@click.option("--path", type=click.STRING, default=".", help="项目生成目标路径")
def _create(name, path):
    """生成指定Dash应用项目模板到指定目录"""

    # 交互式输入配置参数
    click.echo(
        click.style(
            "\n请配置项目参数（直接回车使用默认值）：\n",
            fg="yellow",
        )
    )

    # 从命令行交互式输入获取项目名称
    project_name = click.prompt(
        "项目名称", default=name, type=click.STRING, show_default=True
    )

    # 复制项目模板到指定目录
    shutil.copytree(
        src=os.path.join(
            # magic-dash实际位置
            os.path.dirname(os.path.abspath(__file__)),
            "templates",
            name,
        ),
        dst=os.path.join(path, name),
    )

    # 重命名已生成项目名称
    os.rename(
        src=os.path.join(path, name),
        dst=os.path.join(path, project_name),
    )

    click.echo(
        click.style(
            "已成功生成项目 {} 至目录 {}".format(
                name, os.path.join(path, project_name)
            ),
            fg="green",
        )
    )


# 令子命令生效
magic_dash.add_command(_list)
magic_dash.add_command(_create)

if __name__ == "__main__":
    magic_dash()
