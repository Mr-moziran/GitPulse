import unittest
import pandas as pd
import os
import shutil
from src.visualizer import RepoVisualizer


class TestVisualizer(unittest.TestCase):
    def setUp(self):
        self.csv_path = "tests/test_viz.csv"
        self.out_dir = "tests/out_img"

        # 创建一个用于测试的小型 CSV
        df = pd.DataFrame({
            'author': ['Dev A', 'Dev B', 'Dev A'],
            'date': ['2024-01-01', '2024-02-01', '2024-03-01'],
            'insertions': [100, 200, 300],
            'deletions': [50, 50, 50],
            'message': ['feat: login', 'fix: bug', 'docs: update']
        })
        df.to_csv(self.csv_path, index=False)

        self.viz = RepoVisualizer(self.csv_path, self.out_dir)

    def test_output_directory_creation(self): # 第一个测试方法
        """测试是否会自动创建输出目录"""


    def test_images_generated(self):  # 第二个测试方法
        """测试核心图表是否生成"""


    def tearDown(self):
        """清理方法"""
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)
        if os.path.exists(self.out_dir):
            shutil.rmtree(self.out_dir)


if __name__ == '__main__':
    unittest.main()