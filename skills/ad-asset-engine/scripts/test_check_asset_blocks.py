import unittest
from check_asset_blocks import validate

ROLE = '''【角色四格设定图】
16:9，全图共4格，面部特写、正面全身、90°侧面全身、背面全身。
【五官10项锁定】脸型、眉形等具体描述。
三格无脸，头顶至鞋完整入画。图底声纹波形。
画面正上方居中写着唯一文字：“云若”，绝对禁止输出任何其他英文字母、乱码或多余文字。
negative prompt: extra fifth panel, different face, handheld props
'''
BASE = '【场景母版】\n16:9，无人空镜。\n【空间坐标】门在南，药柜在北。\n【主光源】北窗月光。'
GRID = '''【场景定位】药铺室内，16:9，全图共9格。
【场景画面描写】南门朝北看药柜。
【九宫格内容分配】模式A，同一空间。
【参考场景锁定模式】只移动摄影机。
【摄影机矩阵】1至9各观察方向。
【摄影机参数】50mm。
【光照曝光】月光保留细节。
【标注要求】中文失败改数字1至9和图外对照表。
无人空镜。
'''
PROP = '【道具设定图】16:9，全图共4格。正面视图、45°侧视图、顶部俯视图、关键细节特写。左上角标注：铜钥匙。无人物、无手，禁止手持。'

def doc(body,voice=False):
    prefix='## 资产名（图1）\n'
    if voice: prefix+='Voice Description：An older male voice, low pitch. Calm and measured for short drama.\nVoice Description Label：Low warm measured voice\n'
    return prefix+'```text\n'+body+'\n```\n'

class Tests(unittest.TestCase):
    def test_all_asset_types(self):
        for body in (BASE,GRID,PROP): self.assertEqual(validate(doc(body)),[])
        self.assertEqual(validate(doc(ROLE,True)),[])
    def test_ratio_adjacent_to_chinese(self):self.assertEqual(validate(doc(BASE.replace('16:9','整板16:9横版'))),[])
    def test_no_hidden_reference(self):self.assertTrue(validate(doc(BASE+'\n布局同上。')))
    def test_no_image_number_in_prompt(self):self.assertTrue(validate(doc(BASE+'\n参考图1。')))
    def test_scene_grid_required_fields(self):self.assertTrue(validate(doc(GRID.replace('【光照曝光】',''))))
    def test_four_panel_not_five(self):self.assertTrue(validate(doc(ROLE.replace('全图共4格','全图共5格'),True)))
    def test_voice_text_must_exist(self):self.assertTrue(validate(doc(ROLE)))
    def test_missing_character_name(self):
        self.assertTrue(validate(doc(ROLE.replace('画面正上方居中写着唯一文字：“云若”，绝对禁止输出任何其他英文字母、乱码或多余文字。',''),True)))
    def test_name_must_be_top_center(self):
        self.assertTrue(validate(doc(ROLE.replace('画面正上方居中','画面左下方'),True)))
    def test_no_rendered_voice_label(self):
        self.assertTrue(validate(doc(ROLE+'图底音色速览标签：Low warm measured voice\n',True)))
    def test_no_conflicting_name_negative(self):
        self.assertTrue(validate(doc(ROLE+'negative prompt: character names\n',True)))
    def test_name_cannot_be_placeholder(self):
        self.assertTrue(validate(doc(ROLE.replace('“云若”','“角色名称”'),True)))
    def test_prop_no_hands(self):self.assertTrue(validate(doc(PROP.replace('无人物、无手，禁止手持。',''))))
    def test_missing_template_type(self):self.assertTrue(validate(doc('16:9，全图共4格，不知道是哪类。')))
    def test_multiple_blocks(self):self.assertEqual(validate(doc(BASE)+doc(PROP)),[])
    def test_local_independence(self):self.assertTrue(validate(doc(BASE+'\n按外部技能的模板执行。')))

if __name__=='__main__':unittest.main()
