import os
import unittest

from src.miner import RepoMiner


class TestRepoMiner(unittest.TestCase):
    def setUp(self):
        self.test_csv = "tests/temp_data.csv"
        # 注意：这里我们只测初始化和保存逻辑，不测真实的 Git 抓取（因为太慢）
        self.miner = RepoMiner("dummy_path", self.test_csv)

    def test_init_params(self):
        """测试初始化参数是否正确赋值"""
        self.assertEqual(self.miner.repo_path, "dummy_path")
        self.assertEqual(self.miner.output_path, self.test_csv)

    def test_save_csv_structure(self):
        """测试 CSV 保存结构是否完整"""
        # 构造假数据
        fake_data = [{
            'hexsha': '1a2b3c',
            'author': 'Tester',
            'email': 'test@test.com',
            'date': '2024-01-01',
            'message': 'Initial commit',
            'insertions': 10,
            'deletions': 2,
            'files_changed': 1
        }]

        self.miner._save_to_csv(fake_data)

        # 验证文件是否存在
        self.assertTrue(os.path.exists(self.test_csv))

        # 验证文件内容（简单的读取检查）
        with open(self.test_csv, 'r', encoding='utf-8') as f:
            header = f.readline().strip()
            self.assertIn('hexsha', header)
            self.assertIn('author', header)

    def tearDown(self):
        # 清理测试生成的临时文件
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)


if __name__ == '__main__':
    unittest.main()
