import unittest

from src.hatch_project.scraping import Scp
# from hatch_project import Scp
# from scraping import Scp


class ScpTest(unittest.TestCase):

    # -----上級編----------
    def setUp(self):
        # クラスを初期化
        self.scp = Scp()
        print('初期化')

    def tearDown(self):
        # クラスを削除
        del self.scp
        print('削除')

    def test_set_url_and_tag(self):
        url = 'https://zerofromlight.com/blogs/'
        tag = 'h5'
        datas = self.scp.set_url_and_tag(url, tag)
        # データ型の判定
        self.assertIsInstance(datas, list,
                '戻り値はリスト型である')

    def test_set_url_and_tag_raise(self):
        no_https_url = 'zerofromlight.com/blogs'
        tag = 'h5'
        with self.assertRaisesRegex(ValueError,
                'Invalid URL:Example is https://example.com/.'):
            self.scp.set_url_and_tag(no_https_url, tag)
