"""Check the explicit timing syntax documented in references/output-format.md.

This checks text structure and scheduled audio, not semantic source coverage,
actual speaking performance, asset availability, or model generation quality.
"""
import argparse
from decimal import Decimal
from pathlib import Path
import re

FIELDS = ['场号', '风格', '场景', '站位参考', '角色声音', '镜头', '负面']
NUMBER = r'(\d+(?:\.\d+)?)'
FIELD = re.compile(r'^(' + '|'.join(FIELDS) + r')：(.*)$')
SHOT = re.compile(r'^镜头(\d+)（' + NUMBER + '—' + NUMBER + '秒，' + NUMBER + '秒）：(.+)$')
AUDIO = re.compile(r'^(对白|旁白|心声|画外音)（' + NUMBER + '—' + NUMBER + r'秒，([^）]+)）：(.+)$')


def chinese_number(n):
    if n < 10:
        return '一二三四五六七八九'[n - 1]
    if n < 20:
        return '十' + ('' if n == 10 else '一二三四五六七八九'[n % 10 - 1])
    return '一二三四五六七八九'[n // 10 - 1] + '十' + ('' if n % 10 == 0 else '一二三四五六七八九'[n % 10 - 1])


def validate_case(text, seconds):
    if seconds not in (15, 30):
        return ['目标时长只能是15或30秒']
    blocks = re.findall(r'```(?:swift|text)?\n(.*?)\n```', text, re.S)
    if not blocks:
        blocks = [text.strip()]
    errors = []
    shot_pattern = re.compile(r'^镜头([一二三四五六七八九十百0-9]+)：（(\d+(?:\.\d+)?)秒）(.+)$')
    for index, block in enumerate(blocks, 1):
        prefix = f'第{index}段：'
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 5 or not all(lines[k].startswith(name + '：') for k, name in enumerate(('风格', '场景', '站位参考'))):
            errors.append(prefix + '须以风格、场景、站位参考开头')
            continue
        if not lines[-1].startswith('负面：'):
            errors.append(prefix + '末行须为负面')
        total = Decimal(0)
        number = 0
        dialogue = narration = 0
        in_shots = False
        for line in lines[3:-1]:
            if not in_shots and re.match(r'^[^：]+声音：@.+$', line) and not line.startswith('角色声音：'):
                continue
            match = shot_pattern.match(line)
            if not match:
                errors.append(prefix + '不可识别的声音或镜头行：' + line[:35])
                continue
            in_shots = True
            ordinal, duration, body = match.groups()
            number += 1
            if ordinal != chinese_number(number):
                errors.append(prefix + '镜头须按中文数字从一递增')
            duration = Decimal(duration)
            if duration <= 0:
                errors.append(prefix + '镜头时长须为正')
            total += duration
            required = Decimal(0)
            for quote in re.finditer(r'“([^”]*)”|"([^"\n]*)"', body):
                spoken = quote.group(1) if quote.group(1) is not None else quote.group(2)
                count = sum(c.isalnum() for c in spoken)
                lead = body[max(0, quote.start()-12):quote.start()]
                rate = Decimal(6 if re.search(r'(旁白|心声)[^“”"]*$', lead) else 5)
                required += Decimal(count) / rate
                if rate == 6:
                    narration += count
                else:
                    dialogue += count
            if required > duration:
                errors.append(prefix + f'镜头{ordinal}混合语音超出镜头时长')
        if not number or total != seconds:
            errors.append(prefix + f'镜头总时长为{total}，应为{seconds}秒')
        if dialogue > (80 if seconds == 15 else 160) or narration > (90 if seconds == 15 else 180):
            errors.append(prefix + '段级语音字数超限')
    return errors


def validate(text, seconds):
    if re.search(r'^镜头[一二三四五六七八九十百]+：', text, re.M):
        return validate_case(text, seconds)
    errors = []
    if seconds not in (15, 30):
        return ['目标时长只能是15或30秒']
    lines = [x.strip() for x in text.splitlines() if x.strip() and not x.strip().startswith('```')]
    blocks = []
    for line in lines:
        if line.startswith('场号：'):
            blocks.append([])
        if not blocks:
            errors.append('代码块内首个字段须为场号')
            continue
        blocks[-1].append(line)
    if not blocks:
        return errors + ['未找到分段']
    ids = set()
    target = Decimal(seconds)
    for index, block in enumerate(blocks, 1):
        label = block[0].split('：', 1)[1]
        prefix = f'第{index}段({label})'
        def err(message):
            errors.append(prefix + '：' + message)
        if not label or label in ids:
            err('场号为空或重复')
        ids.add(label)
        names, content = [], {}
        current = None
        for line in block:
            match = FIELD.match(line)
            if match:
                current, value = match.groups()
                names.append(current)
                content.setdefault(current, []).append(value)
            elif current:
                content[current].append(line)
        if names != FIELDS:
            err('七字段须各出现一次，按场号、风格、场景、站位参考、角色声音、镜头、负面排序')
        for name in FIELDS:
            if name != '镜头' and not ''.join(content.get(name, [])).strip():
                err(name + '为空')
        shots, audio = [], []
        for line in content.get('镜头', []):
            if not line:
                continue
            m = SHOT.match(line)
            if m:
                number, start, end, duration, description = m.groups()
                start, end, duration = map(Decimal, (start, end, duration))
                if number != str(len(shots) + 1):
                    err('镜号必须从1递增')
                if duration <= 0 or end - start != duration:
                    err('镜头时长标签与起止时间不符')
                if start != (shots[-1][1] if shots else Decimal(0)):
                    err('镜头时间轴存在空隙、重叠或未从0开始')
                shots.append((start, end, duration))
                continue
            m = AUDIO.match(line)
            if m:
                kind, start, end, speaker, speech = m.groups()
                start, end = map(Decimal, (start, end))
                if not Decimal(0) <= start < end <= target:
                    err('语音起止越界或时长不为正')
                count = sum(c.isalnum() for c in speech)
                rate = Decimal(6 if kind in ('旁白', '心声') else 5)
                if count > (end - start) * rate:
                    err(f'{speaker}的{kind}有{count}个有效字符，超出语音窗口预算')
                voice = '\n'.join(content.get('角色声音', []))
                if speaker not in voice:
                    err(f'角色声音字段缺少{speaker}')
                audio.append((start, end, kind, count))
                continue
            err('镜头或语音行格式不可识别：' + line[:50])
        if not shots or shots[-1][1] != target or sum((x[2] for x in shots), Decimal(0)) != target:
            err(f'镜头须连续覆盖0至{seconds}秒，总时长恰好{seconds}秒')
        ordered = sorted(audio)
        for previous, following in zip(ordered, ordered[1:]):
            if following[0] < previous[1]:
                err('对白、旁白和心声共享时间轴，语音重叠')
        voice = '\n'.join(content.get('角色声音', [])).strip()
        if voice == '无' and audio:
            err('有语音时角色声音不能为无')
        if voice and voice != '无' and not audio:
            err('已声明角色声音但没有可校验的语音时间行')
        dialogue = sum(n for _, _, kind, n in audio if kind in ('对白', '画外音'))
        narration = sum(n for _, _, kind, n in audio if kind in ('旁白', '心声'))
        if dialogue > (80 if seconds == 15 else 160):
            err('对白总字数超段上限')
        if narration > (90 if seconds == 15 else 180):
            err('旁白与心声总字数超段上限')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--seconds', required=True, type=int, choices=(15, 30))
    args = parser.parse_args()
    errors = validate(args.file.read_text(encoding='utf-8'), args.seconds)
    if errors:
        for message in errors:
            print('FAIL:', message)
        return 1
    print(f'PASS: 提示词结构、镜头时长与混合语音预算通过（{args.seconds}秒版）；仍需人工核对原文覆盖和实际表演。')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
