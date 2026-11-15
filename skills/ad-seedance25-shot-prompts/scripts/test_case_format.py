import unittest
from validate_prompt import validate

def prompt(t=30,body=None):
 return '```swift\n风格：架空修仙；3D国漫CG；电影光影。\n场景：山门[@山门]；日/晴；石阶；云若[@云若]面向苍珏[@苍珏]。\n站位参考：@\n云若声音：@A clear young female voice.\n'+(body or f'镜头一：（{t}秒）近景，平视，固定；云若[@云若]：“我想试。”')+'\n负面：不要bgm，不要字幕\n```'
class Tests(unittest.TestCase):
 def test_accept_reference_shape(self):self.assertEqual(validate(prompt(),30),[])
 def test_accept_15(self):self.assertEqual(validate(prompt(15),15),[])
 def test_wrong_sum(self):self.assertTrue(validate(prompt(15),30))
 def test_mixed_voice_budget(self):
  b='镜头一：（15秒）近景；云若[@云若]：“'+'字'*50+'”；旁白：“'+'字'*60+'”'
  self.assertTrue(validate(prompt(15,b),15))
 def test_no_internal_headers(self):self.assertTrue(validate(prompt().replace('站位参考：@','站位参考：@\n角色声音：聚合'),30))
 def test_sequential_chinese_shot_numbers(self):self.assertTrue(validate(prompt(body='镜头二：（30秒）固定；风吹。'),30))
if __name__=='__main__':unittest.main()
