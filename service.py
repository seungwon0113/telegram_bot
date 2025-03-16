from database import Database

class ScheduleService:
    def __init__(self):
        self.db = Database()
    
    # 일정 추가
    async def add_schedule(self, user_id: int, date: str, content: str) -> str:
        try:
            if self.db.add_schedule(user_id, date, content):
                return f"일정이 추가되었습니다!\n날짜: {date}\n내용: {content}"
            return "일정 추가에 실패했습니다."
        except Exception:
            return "일정 추가 실패! 형식을 확인해주세요.\n예: /add 2024-03-20 점심약속"

    # 일정 조회    
    async def list_schedules(self, user_id: int) -> str:
        schedules = self.db.get_schedules(user_id)
        
        if not schedules:
            return "등록된 일정이 없습니다."
        
        response = "📅 일정 목록:\n\n"
        for schedule in schedules:
            response += f"#{schedule[0]} - {schedule[1]}: {schedule[2]}\n"
        return response
    
    # 일정 삭제
    async def delete_schedule(self, schedule_id: str, user_id: int) -> str:
        try:
            if self.db.delete_schedule(int(schedule_id), user_id):
                return f"#{schedule_id} 일정이 삭제되었습니다."
            return "해당 일정을 찾을 수 없습니다."
        except:
            return "삭제 실패! 형식을 확인해주세요.\n예: /delete 1"
    
    # 기본 메세지 처리
    async def handle_message(self, text: str) -> str:
        text = text.lower()
        if "안녕" in text:
            return "안녕하세요! 일정 관리를 도와드릴 수 있습니다."
        elif "일정" in text:
            return ("일정을 관리하시려면 다음 명령어를 사용해주세요:\n"
                   "/add - 일정 추가\n"
                   "/list - 일정 목록\n"
                   "/delete - 일정 삭제")
        return "죄송하지만 이해하지 못했습니다. /start 를 입력하여 사용 가능한 명령어를 확인해주세요."
