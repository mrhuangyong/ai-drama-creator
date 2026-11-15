import re
from pathlib import Path
import unittest
from check_combat_prompt import validate

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        s=(Path(__file__).resolve().parents[1]/'references/output-format.md').read_text()
        cls.example=re.search(r'```swift\n(.*?)\n```',s,re.S)[1]
    def test_fifteen(self):self.assertEqual(validate(self.example,15),[])
    def test_wrong_duration(self):self.assertTrue(validate(self.example,30))
    def test_missing_scene(self):self.assertTrue(validate(self.example.replace('场景：','环境：'),15))
    def test_repeated_shot(self):self.assertTrue(validate(self.example.replace('镜头二','镜头一'),15))
    def test_decimal(self):self.assertTrue(validate(self.example.replace('（3秒）','（2.5秒）',1),15))
    def test_engine_marker(self):self.assertTrue(validate(self.example.replace('火花','模式K火花'),15))
    def test_broken_timeline(self):
        t='风格：3D\n场景：石桥\n站位参考：@\n0-3秒左方攻来。\n4-15秒右方挡开。\n负面：不要bgm，不要字幕。'
        self.assertTrue(validate(t,15))
    def test_thirty_timeline(self):
        t='风格：3D\n场景：石桥\n站位参考：@\n0-3秒左方攻来。\n3-30秒右方挡开。\n负面：不要bgm，不要字幕。'
        self.assertEqual(validate(t,30),[])
    def test_one_take(self):
        t='风格：3D\n场景：石桥\n站位参考：@\n镜头一：（15秒）连续跟拍；0-3秒来袭，3-9秒格挡，9-15秒缴械收束。\n负面：不要bgm，不要字幕。'
        self.assertEqual(validate(t,15),[])
        self.assertTrue(validate(t.replace('格挡','硬切格挡'),15))
    def test_thirty_shots(self):
        # Distinct sequence, not re-labelling a 15-second sample as 30 seconds.
        header='风格：3D国漫\n场景：冰殿北榻、南门、西侧后殿门，神明在北、敌人在南。\n站位参考：@\n'
        actions=['敌人由南门进逼，步履踏碎薄霜','窄刃刺向北榻，守方侧转半步','两指夹住刀刃，刃尖停在衣领前','寒气沿金属纹理爬到护手，刀身碎落','攻方右臂被冰封，失衡滑退至东柱','家主推出火轮，轮缘火焰刮向北阶','守方转腕张掌，薄蓝霜层从轮缘合拢','火轮熄灭崩碎，金属残片落在阶下','家主踉跄退步扶住胸前，神明仍未离开北榻','守方踏上阶前挡住通路，敌人停步、碎冰落地，保护目标完成']
        t=header+'\n'.join(f'镜头{i+1}：（3秒）中景，斜侧跟拍；{a}。' for i,a in enumerate(actions))+'\n负面：不要bgm，不要字幕，不要水印。'
        self.assertEqual(validate(t,30),[])

if __name__=='__main__':unittest.main()
