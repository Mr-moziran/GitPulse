import csv
import os
from git import Repo
from datetime import datetime

class RepoMiner:
    """
    TODO: 组员A 待实现
    负责挖掘 Git 仓库日志
    """
    def __init__(self, repo_path, output_path):
        """
        初始化挖掘器
        :param repo_path: 本地 Git 仓库路径
        :param output_path: 输出 CSV 文件路径
        """
        self.repo_path = repo_path
        self.output_path = output_path

    def analyze(self):
        print(f"[Miner] 正在分析仓库: {self.repo_path} ...")
        
        if not os.path.exists(self.repo_path):
            raise FileNotFoundError(f"找不到仓库路径: {self.repo_path}")

        try:
            repo = Repo(self.repo_path)
        except Exception as e:
            raise ValueError(f"路径不是有效的 Git 仓库: {e}")
        
        data = []
        # 针对 GPT-SoVITS，我们分析所有分支，不设数量限制
        print("[Miner]正在读取 Git 日志，这可能需要几秒钟...")
        commits = list(repo.iter_commits(all=True))
        print(f"[Miner] 共发现 {len(commits)} 条提交记录，正在提取特征...")

        for i, commit in enumerate(commits):
            # 每处理 500 条打印一次进度
            if i % 500 == 0:
                print(f"  - 处理进度: {i}/{len(commits)}")

            try:
                stats = commit.stats.total
                insertions = stats.get('insertions', 0)
                deletions = stats.get('deletions', 0)
                lines = stats.get('lines', 0)
            except:
                # 处理合并提交可能没有 stats 的情况
                insertions = 0
                deletions = 0
                lines = 0

            data.append({
                'hexsha': commit.hexsha,
                'author': commit.author.name,
                'email': commit.author.email,
                'date': datetime.fromtimestamp(commit.committed_date),
                'message': commit.message.strip(),
                'insertions': insertions,
                'deletions': deletions,
                'files_changed': lines
            })

        self._save_to_csv(data)
        return self.output_path

    def _save_to_csv(self, data):
        if not data:
            print("[Miner] 警告：没有抓取到任何数据！")
            return

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        
        keys = data[0].keys()
        with open(self.output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
            
        print(f"[Miner] 数据挖掘完成！已保存至: {self.output_path}")