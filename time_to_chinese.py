#!/usr/bin/env python3
"""
把时间转换成中文口语读法
例：14:30 -> "下午两点半"
"""

from datetime import datetime


def _num_to_cn(n: int) -> str:
    """把 0~59 之间的数字转成中文读法，比如 5 -> 五，15 -> 十五，30 -> 三十"""
    digits = "零一二三四五六七八九"
    if n == 0:
        return "零"
    if n < 10:
        return digits[n]
    tens, unit = divmod(n, 10)
    tens_str = "十" if tens == 1 else digits[tens] + "十"
    unit_str = digits[unit] if unit != 0 else ""
    return tens_str + unit_str


def time_to_chinese(dt: datetime = None) -> str:
    """把时间转换成中文口语读法，比如 14:30 -> '下午两点半'"""
    if dt is None:
        dt = datetime.now()

    hour, minute = dt.hour, dt.minute

    if hour < 5:
        period = "凌晨"
    elif hour < 9:
        period = "早上"
    elif hour < 12:
        period = "上午"
    elif hour == 12:
        period = "中午"
    elif hour < 18:
        period = "下午"
    else:
        period = "晚上"

    hour_12 = hour % 12
    if hour_12 == 0:
        hour_12 = 12

    hour_cn = "两" if hour_12 == 2 else _num_to_cn(hour_12)

    if minute == 0:
        minute_part = "点"
    elif minute == 30:
        minute_part = "点半"
    elif minute == 15:
        minute_part = "点一刻"
    elif minute == 45:
        minute_part = "点三刻"
    elif minute < 10:
        minute_part = f"点零{_num_to_cn(minute)}分"
    else:
        minute_part = f"点{_num_to_cn(minute)}分"

    return f"{period}{hour_cn}{minute_part}"


if __name__ == "__main__":
    # 验证题目给的例子
    test_cases = [
        (datetime(2026, 1, 1, 14, 30), "下午两点半"),
        (datetime(2026, 1, 1, 0, 5), None),
        (datetime(2026, 1, 1, 9, 15), None),
        (datetime(2026, 1, 1, 18, 45), None),
        (datetime(2026, 1, 1, 12, 0), None),
    ]
    for dt, expected in test_cases:
        result = time_to_chinese(dt)
        mark = "✓" if expected is None or result == expected else "✗"
        print(f"{mark} {dt.strftime('%H:%M')} -> {result}")

    print("\n现在是：", time_to_chinese())
