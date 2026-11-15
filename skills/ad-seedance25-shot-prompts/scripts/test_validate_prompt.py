import unittest
from validate_prompt import validate


def block(seconds=15, audio='', shots=None):
    voice = '阿宁：@青年女声，清晰克制。' if audio else '无'
    shots = shots or f'镜头1（0—{seconds}秒，{seconds}秒）：中景，固定镜头；阿宁站在门内。'
    return f'''场号：一场01
风格：现代悬疑；真人写实；低照度冷光。
场景：仓库门内；夜/阴；铁门关闭；阿宁站在门内面向铁门。
站位参考：@
角色声音：{voice}
镜头：
{shots}
{audio}
负面：严格参考角色图生成角色形象，禁止出现明星脸，不要bgm，不要字幕、标题或额外文字叠层
'''


class TimingTests(unittest.TestCase):
    def test_valid_15_and_30(self):
        for seconds in (15, 30):
            with self.subTest(seconds=seconds):
                self.assertEqual(validate(block(seconds, '对白（1—3秒，阿宁）：不要开门。'), seconds), [])

    def test_reaction_cut_can_carry_one_continuous_voice(self):
        shots = '镜头1（0—5秒，5秒）：近景，阿宁说话。\n镜头2（5—6秒，1秒）：听者反应。\n镜头3（6—15秒，9秒）：回到阿宁。'
        self.assertEqual(validate(block(audio='对白（0—10秒，阿宁）：' + '我'*40, shots=shots), 15), [])

    def test_wrong_mode(self):
        self.assertTrue(validate(block(30), 15))

    def test_gap_even_when_durations_sum_to_target(self):
        shots = '镜头1（0—7秒，7秒）：近景。\n镜头2（8—16秒，8秒）：全景。'
        self.assertTrue(validate(block(shots=shots), 15))

    def test_duration_label_must_match_interval(self):
        self.assertTrue(validate(block(shots='镜头1（0—15秒，14秒）：近景。'), 15))

    def test_dialogue_cannot_use_full_80_char_cap_in_15_seconds(self):
        self.assertTrue(validate(block(audio='对白（0—15秒，阿宁）：' + '字'*80), 15))

    def test_mixed_audio_shares_time(self):
        audio = '对白（0—10秒，阿宁）：' + '字'*50 + '\n旁白（8—15秒，旁白）：' + '字'*42
        self.assertTrue(validate(block(audio=audio), 15))

    def test_missing_voice_track(self):
        self.assertTrue(validate(block(audio='阿宁说：“不要开门。”'), 15))

    def test_silent_segment(self):
        self.assertEqual(validate(block().replace('角色声音：阿宁：@青年女声，清晰克制。', '角色声音：无'), 15), [])

    def test_missing_and_duplicate_fields(self):
        self.assertTrue(validate(block().replace('站位参考：@\n', ''), 15))
        self.assertTrue(validate(block().replace('风格：', '风格：重复\n风格：'), 15))

    def test_multiple_segments(self):
        text = block() + '\n' + block().replace('一场01', '一场02')
        self.assertEqual(validate(text, 15), [])

    def test_duplicate_segment_id(self):
        self.assertTrue(validate(block() + '\n' + block(), 15))

    def test_half_second_shots(self):
        shots='镜头1（0—0.5秒，0.5秒）：手部特写。\n镜头2（0.5—15秒，14.5秒）：固定镜头。'
        self.assertEqual(validate(block(shots=shots),15), [])


if __name__ == '__main__':
    unittest.main()
