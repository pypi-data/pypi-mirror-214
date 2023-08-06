from fire import Fire

from chainfury.base import logger


def _main():
    "🦋 ChainFury Engine CLI"
    print(
        """
🦋 Welcome to ChainFury Engine!

A powerful way to program for the "Software 2.0" era. Read more:

- https://blog.nimblebox.ai/new-flow-engine-from-scratch
- https://blog.nimblebox.ai/fury-actions
- https://gist.github.com/yashbonde/002c527853e04869bfaa04646f3e0974

🌟 us on https://github.com/NimbleBoxAI/ChainFury

Build with ♥️  by NimbleBox.ai

🌊 Chennai, India
"""
    )


def main():
    Fire(_main)
