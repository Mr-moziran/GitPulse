## GitPulse

**GitPulse**是一款轻量级的Git仓库静态分析工具。它旨在通过自动化挖掘 Git 提交日志（Commit
Log），提取项目的演化特征，并通过可视化图表揭示开源社区的协作模式与代码质量趋势。

### 核心功能

- 全面挖掘：基于`GitPython`库遍历目标仓库的.git对象，全面提取各种数据特征，尤其包含insertions/deletions，并将非结构化日志转成结构化文件存储
- 多维度可视化分析：囊括仓库每月提交活跃度，每月代码变动规模，核心贡献者等多维度图表

### 快速开始

推荐使用Anaconda管理环境，避免依赖冲突：

~~~shell
git pull git@github.com:Mr-moziran/GitPulse.git
cd GitPulse
conda create -n gitpulse python==3.13
conda activate gitpulse
pip install -r requirements.txt
~~~
