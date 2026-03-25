#!/bin/bash
docker exec -i court-slay-2001-app-1 python3 << 'EOF'
import asyncio
from notifier import run_notifier
from bot import build_bot
import os
bot = build_bot(os.getenv('BOT_TOKEN')).bot
asyncio.run(run_notifier(bot))
EOF
