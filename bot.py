from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio
from dotenv import load_dotenv
import os
import nest_asyncio
from service import ScheduleService

# nest_asyncio 적용
nest_asyncio.apply()
load_dotenv()

class TelegramBot:
    def __init__(self):
        self.service = ScheduleService()
    
    async def start(self, update, context):
        await update.message.reply_text(
            "안녕하세요! 일정 관리 봇입니다.\n"
            "다음 명령어를 사용할 수 있습니다:\n"
            "/add 2024-03-20 점심약속 - 새로운 일정 추가\n"
            "/list - 모든 일정 보기\n"
            "/delete 1 - 1번 일정 삭제"
        )
    
    async def add_schedule(self, update, context):
        # 메세지가 없는경우
        if not update.message:
            return
            
        try:
            date = context.args[0]
            content = ' '.join(context.args[1:])
            response = await self.service.add_schedule(
                update.effective_user.id, 
                date, 
                content
            )
            await update.message.reply_text(response)
        except (IndexError, AttributeError):  # 구체적인 예외 처리
            await update.message.reply_text("일정 추가 실패! 형식을 확인해주세요.\n예: /add 2024-03-20 점심약속")
    
    async def list_schedules(self, update, context):
        if not update.message:
            return
        response = await self.service.list_schedules(update.effective_user.id)
        await update.message.reply_text(response)
    
    async def delete_schedule(self, update, context):
        if not update.message:
            return
            
        try:
            response = await self.service.delete_schedule(
                context.args[0],
                update.effective_user.id
            )
            await update.message.reply_text(response)
        except (IndexError, AttributeError):  # 구체적인 예외 처리
            await update.message.reply_text("삭제 실패! 형식을 확인해주세요.\n예: /delete 1")
    
    async def handle_message(self, update, context):
        if not update.message:
            return
            
        print(f"메시지 받음: {update.message.text}")
        response = await self.service.handle_message(update.message.text)
        await update.message.reply_text(response)
    
    async def run(self):
        token = os.environ.get("TELEGRAM_TOKEN")
        app = Application.builder().token(token).build()
        
        # 명령어 핸들러 등록
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("add", self.add_schedule))
        app.add_handler(CommandHandler("list", self.list_schedules))
        app.add_handler(CommandHandler("delete", self.delete_schedule))
        
        # 일반 메시지 핸들러 등록
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        print("봇이 시작되었습니다...")
        
        # 봇 실행
        await app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    try:
        bot = TelegramBot()
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("봇이 종료되었습니다.") 