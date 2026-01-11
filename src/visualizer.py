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

