import asyncio
from core.conversation import Conversation


CSI = "\x1b["
RESET = CSI + "0m"

def fg_256(n):
    return f"{CSI}38;5;{n}m"

def gradient_text(text, start=196, end=226):
    res = []
    L = len(text)
    for i, ch in enumerate(text):
        color = int(start + (end - start) * i / max(1, L - 1))
        res.append(fg_256(color) + ch)
    return "".join(res) + RESET

def welcome():
    border_color = fg_256(33)
    star1 = fg_256(226) + "✦" + RESET
    star2 = fg_256(220) + "✧" + RESET

    # 顶部星空边框
    border = border_color + "═" * 50 + RESET
    print("\n " + border)
    print("  " + (star1 + " ") * 5 + (star2 + " ") * 5)

    # 渐变欢迎语
    text = gradient_text("★ Welcome to Quick Star ★", 196, 226)
    print("\n" + text.center(55))

    # 底部星空
    print("\n  " + (star2 + " ") * 5 + (star1 + " ") * 5)
    print(" " + border + "\n")

async def main():
    welcome()
    await Conversation().start_conversation()


def cli():
    """同步入口点，供 pyproject.toml 使用"""
    asyncio.run(main())

if __name__ == "__main__":
    cli()