from database import Database
import smtplib, os
from email.mime.text import MIMEText

class ScheduleService:
    def __init__(self):
        self.db = Database()
    
    # 일정 추가
    async def add_schedule(self, user_id: int, date: str, content: str) -> str:
        try:
            if self.db.add_schedule(user_id, date, content):
                return f"일정이 추가되었습니다!\n날짜: {date}\n내용: {content}"
            return "일정 추가에 실패했습니다."
        except Exception as e:
            return f"일정 추가 실패! 오류: {str(e)}\n예: /add 2024-03-20 점심약속"

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
        
    # 메일 보내기
    async def send_mail(self, to_email: str, subject: str, body: str) -> str:
        try:
            google_mail = os.environ.get('GOOGLE_EMAIL')
            google_app = os.environ.get('GOOGLE_APP')
            
            
            if not all([google_mail, google_app, to_email]):
                return "이메일 설정이 올바르지 않습니다. 환경변수를 확인해주세요."

            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.ehlo()
            smtp.starttls()
            
            try:
                smtp.login(google_mail, google_app)
            except smtplib.SMTPAuthenticationError as e:
                return f"Gmail 로그인 실패: {str(e)}"

            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = google_mail
            msg['To'] = to_email

            try:
                smtp.sendmail(google_mail, to_email, msg.as_string())
            except Exception as e:
                return f"이메일 전송 실패: {str(e)}"
            finally:
                smtp.quit()
            
            return "이메일이 성공적으로 전송되었습니다."
            
        except Exception as e:
            return f"이메일 전송 중 오류가 발생했습니다: {str(e)}"
    
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
