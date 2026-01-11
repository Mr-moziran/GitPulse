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