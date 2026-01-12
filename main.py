import click

from src.miner import RepoMiner
from src.visualizer import RepoVisualizer


@click.command()
@click.option('--repo', default='./GPT-SoVITS', help='目标 Git 仓库的本地路径 (e.g. ./GPT-SoVITS)')
@click.option('--output', default='./data/commits.csv', help='中间数据保存路径')
@click.option('--img_dir', default='./report_images', help='图表输出目录')
def main(repo, output, img_dir):
    """
    GitPulse: 基于 Python 的开源软件演化分析工具

    用于分析 GPT-SoVITS 等开源项目的提交历史、活跃度与代码演化。
    """
    click.echo("=" * 60)
    click.echo(f"GitPulse 分析工具启动")
    click.echo(f"目标仓库: {repo}")
    click.echo("=" * 60)

    # 1. 挖掘阶段
    try:
        miner = RepoMiner(repo, output)
        miner.analyze()
    except Exception as e:
        click.echo(f"\n[Error] 挖掘阶段发生错误: {e}")
        return

    # 2. 可视化阶段
    try:
        viz = RepoVisualizer(output, img_dir)
        viz.run_all()
    except Exception as e:
        click.echo(f"\n[Error] 可视化阶段发生错误: {e}")
        return

    click.echo("=" * 60)
    click.echo(f"分析完成！请打开 {img_dir} 查看分析图表。")
    click.echo("=" * 60)


if __name__ == '__main__':
    main()
