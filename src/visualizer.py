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