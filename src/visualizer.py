import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import platform

# --- 字体配置适配 (防止中文乱码) ---
sys_str = platform.system()
if sys_str == 'Windows':
    # Windows 常用中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
elif sys_str == 'Darwin':
    # Mac 常用中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC']
else:
    # Linux 默认字体 (可能需要根据具体环境调整)
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题
plt.style.use('ggplot')  # 使用更好看的绘图风格


class RepoVisualizer:
    def plot_monthly_activity(self, df):
        """图表1: 每月提交活跃度 (折线图)"""
        monthly = df.set_index('date').resample('M').size()

        plt.figure(figsize=(12, 5))
        monthly.plot(kind='line', marker='o', color='green', linewidth=2)
        plt.title('项目提交活跃度趋势 (Commit Activity)')
        plt.ylabel('提交次数')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "1_activity_trend.png"))
        plt.close()

    def plot_top_contributors_by_commits(self, df):
        """图表2: Top 10 贡献者 - 按提交次数 (柱状图)"""
        top = df['author'].value_counts().head(10)

        plt.figure(figsize=(10, 6))
        top.plot(kind='bar', color='steelblue', alpha=0.8)
        plt.title('Top 10 贡献者 (按提交次数)')
        plt.ylabel('Commit Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "2_top_contributors_commits.png"))
        plt.close()

    def plot_top_contributors_by_lines(self, df):
        """图表3: Top 10 贡献者 - 按代码修改行数 (柱状图)"""
        # 计算每个人的总工作量 (新增行数 + 删除行数)
        df['total_changes'] = df['insertions'] + df['deletions']
        top_lines = df.groupby('author')['total_changes'].sum().sort_values(ascending=False).head(10)

        plt.figure(figsize=(10, 6))
        top_lines.plot(kind='bar', color='orange', alpha=0.8)
        plt.title('Top 10 贡献者 (按代码变动行数)')
        plt.ylabel('Total Lines Changed (Add + Del)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "3_top_contributors_lines.png"))
        plt.close()

    def plot_code_churn(self, df):
        """图表4: 每月代码增删规模 (折线图)"""
        churn = df.set_index('date').resample('M')[['insertions', 'deletions']].sum()

        plt.figure(figsize=(12, 5))
        plt.plot(churn.index, churn['insertions'], label='新增代码 (Add)', color='blue', alpha=0.6)
        plt.plot(churn.index, churn['deletions'], label='删除代码 (Del)', color='red', alpha=0.6)
        plt.title('每月代码变动规模 (Code Churn)')
        plt.ylabel('行数')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "4_code_churn.png"))
        plt.close()

    def plot_loc_growth(self, df):
        """图表5: 项目总代码行数增长趋势 (面积图)"""
        # 估算 LOC 增长：新增 - 删除
        df['net_growth'] = df['insertions'] - df['deletions']
        # 按时间排序并计算累积和 (Cumulative Sum)
        df_sorted = df.sort_values('date')
        df_sorted['total_loc'] = df_sorted['net_growth'].cumsum()

        # 按天重采样，取当天的最后值，使曲线平滑
        daily_loc = df_sorted.set_index('date')['total_loc'].resample('D').ffill()

        plt.figure(figsize=(12, 5))
        daily_loc.plot(kind='area', color='purple', alpha=0.3)
        plt.plot(daily_loc.index, daily_loc, color='purple')
        plt.title('项目代码规模增长趋势 (Total LOC Growth)')
        plt.ylabel('累计估算行数')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "5_loc_growth.png"))
        plt.close()

    def plot_bug_fix_trend(self, df):
        """图表6: Bug 修复趋势分析 (已修复日期显示Bug)"""
        # 1. 筛选关键词 (中英文混合)
        keywords = ['fix', 'bug', 'issue', 'crash', 'error', 'solve', '修复', '解决', '问题', '报错']
        pattern = '|'.join(keywords)
        bug_commits = df[df['message'].str.lower().str.contains(pattern, na=False)]

        if len(bug_commits) > 0:
            # 2. 按月统计数量
            bug_trend = bug_commits.set_index('date').resample('M').size()
            bug_trend.index = bug_trend.index.strftime('%Y-%m')

            plt.figure(figsize=(12, 5))
            bug_trend.plot(kind='bar', color='brown', width=0.8, alpha=0.8)
            plt.title('Bug 修复频率 (Bug Fix Frequency)')
            plt.ylabel('修复提交数量 (Commits)')
            plt.xlabel('月份')
            # 旋转 X 轴标签防止重叠
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "6_bug_fix_trend.png"))
            plt.close()
        else:
            print("[Visualizer] 未检测到 Bug 修复相关的提交，跳过 Bug 趋势图。")