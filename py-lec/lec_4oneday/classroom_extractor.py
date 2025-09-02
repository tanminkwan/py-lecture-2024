import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
from datetime import datetime

# OAuth 2.0 scope - Classroom API 접근 권한 (최소 권한으로 시작)
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.students.readonly'
]

# 설정값들 - 실제 값으로 변경 필요
CREDENTIALS_FILE = 'credentials.json'  # Google Cloud에서 다운로드한 JSON 파일 경로
TOKEN_FILE = 'token.pickle'  # 토큰 저장 파일명

def get_classroom_service():
    """인증된 Classroom API 서비스 객체 반환"""
    creds = None
    
    # 기존에 저장된 토큰 로드
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('classroom', 'v1', credentials=creds)
    return service

def list_courses():
    """모든 코스 목록 조회"""
    try:
        service = get_classroom_service()
        results = service.courses().list(pageSize=50).execute()
        courses = results.get('courses', [])
        
        if not courses:
            print('코스를 찾을 수 없습니다.')
            return []
        
        print('📚 사용 가능한 코스들:')
        print('=' * 60)
        
        for i, course in enumerate(courses, 1):
            course_name = course.get('name', '이름 없음')
            course_id = course.get('id', '알 수 없음')
            course_state = course.get('courseState', '알 수 없음')
            
            print(f"{i:2d}. {course_name}")
            print(f"    ID: {course_id}")
            print(f"    상태: {course_state}")
            print("-" * 40)
        
        return courses
        
    except Exception as error:
        print(f'코스 조회 중 오류 발생: {error}')
        return []

def list_coursework(course_id):
    """특정 코스의 과제 목록 조회"""
    try:
        service = get_classroom_service()
        results = service.courses().courseWork().list(courseId=course_id).execute()
        coursework_list = results.get('courseWork', [])
        
        if not coursework_list:
            print(f'코스 ID {course_id}에서 과제를 찾을 수 없습니다.')
            return []
        
        print(f'\n📝 코스의 과제들 (총 {len(coursework_list)}개):')
        print('=' * 60)
        
        for i, work in enumerate(coursework_list, 1):
            title = work.get('title', '제목 없음')
            work_id = work.get('id', '알 수 없음')
            work_type = work.get('workType', '알 수 없음')
            state = work.get('state', '알 수 없음')
            
            # 생성 시간
            creation_time = work.get('creationTime', '')
            if creation_time:
                try:
                    dt = datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    formatted_time = creation_time
            else:
                formatted_time = '알 수 없음'
            
            print(f"{i:2d}. {title}")
            print(f"    ID: {work_id}")
            print(f"    유형: {work_type}")
            print(f"    상태: {state}")
            print(f"    생성일: {formatted_time}")
            print("-" * 40)
        
        return coursework_list
        
    except Exception as error:
        print(f'과제 조회 중 오류 발생: {error}')
        return []

def get_student_submissions(course_id, coursework_id):
    """특정 과제의 학생 제출물들을 가져오기"""
    try:
        service = get_classroom_service()
        
        # 학생 제출물 목록 조회
        submissions = service.courses().courseWork().studentSubmissions().list(
            courseId=course_id,
            courseWorkId=coursework_id,
            pageSize=100
        ).execute().get('studentSubmissions', [])
        
        if not submissions:
            print('제출물을 찾을 수 없습니다.')
            return []
        
        print(f'\n👥 학생 제출물들 (총 {len(submissions)}개):')
        print('=' * 80)
        
        for i, submission in enumerate(submissions, 1):
            user_id = submission.get('userId', '알 수 없음')
            state = submission.get('state', 'UNKNOWN')
            
            # 제출 시간
            creation_time = submission.get('creationTime', '')
            if creation_time:
                try:
                    dt = datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    formatted_time = creation_time
            else:
                formatted_time = '제출 안함'
            
            # 점수
            assigned_grade = submission.get('assignedGrade', '채점 안함')
            
            print(f"{i:2d}. 학생 ID: {user_id}")
            print(f"    상태: {state}")
            print(f"    제출 시간: {formatted_time}")
            print(f"    점수: {assigned_grade}")
            
            # 첨부 파일들
            assignment_submission = submission.get('assignmentSubmission', {})
            attachments = assignment_submission.get('attachments', [])
            
            if attachments:
                print("    📎 첨부 파일들:")
                for j, attachment in enumerate(attachments, 1):
                    if 'driveFile' in attachment:
                        file_info = attachment['driveFile']
                        file_title = file_info.get('title', 'Unknown')
                        file_id = file_info.get('id', 'Unknown')
                        print(f"       {j}. Drive 파일: {file_title} (ID: {file_id})")
                    elif 'link' in attachment:
                        link_url = attachment['link'].get('url', 'Unknown')
                        print(f"       {j}. 링크: {link_url}")
                    elif 'youTubeVideo' in attachment:
                        video_info = attachment['youTubeVideo']
                        video_title = video_info.get('title', 'Unknown')
                        video_url = video_info.get('alternateLink', 'Unknown')
                        print(f"       {j}. YouTube: {video_title} ({video_url})")
            
            print("-" * 60)
        
        return submissions
        
    except Exception as error:
        print(f'제출물 조회 중 오류 발생: {error}')
        return []

def save_submissions_to_json(course_id, coursework_id, filename=None):
    """제출물 데이터를 JSON 파일로 저장"""
    submissions = get_student_submissions(course_id, coursework_id)
    
    if not submissions:
        print("저장할 제출물이 없습니다.")
        return
    
    if filename is None:
        filename = f"submissions_{course_id}_{coursework_id}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(submissions, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 제출물 데이터가 '{filename}' 파일로 저장되었습니다.")
        
    except Exception as error:
        print(f"파일 저장 중 오류 발생: {error}")

def interactive_mode():
    """대화형 모드로 데이터 탐색"""
    print("🎓 Google Classroom 데이터 추출기")
    print("=" * 50)
    
    # 1단계: 코스 목록 조회
    courses = list_courses()
    
    if not courses:
        return
    
    # 2단계: 코스 선택
    while True:
        try:
            choice = input(f"\n조회할 코스 번호를 입력하세요 (1-{len(courses)}, 0=종료): ")
            if choice == '0':
                return
            
            course_index = int(choice) - 1
            if 0 <= course_index < len(courses):
                selected_course = courses[course_index]
                course_id = selected_course['id']
                course_name = selected_course['name']
                print(f"\n✅ 선택된 코스: {course_name} (ID: {course_id})")
                break
            else:
                print("올바른 번호를 입력해주세요.")
        except ValueError:
            print("숫자를 입력해주세요.")
    
    # 3단계: 과제 목록 조회
    coursework_list = list_coursework(course_id)
    
    if not coursework_list:
        return
    
    # 4단계: 과제 선택
    while True:
        try:
            choice = input(f"\n조회할 과제 번호를 입력하세요 (1-{len(coursework_list)}, 0=뒤로): ")
            if choice == '0':
                return
            
            work_index = int(choice) - 1
            if 0 <= work_index < len(coursework_list):
                selected_work = coursework_list[work_index]
                coursework_id = selected_work['id']
                work_title = selected_work['title']
                print(f"\n✅ 선택된 과제: {work_title} (ID: {coursework_id})")
                break
            else:
                print("올바른 번호를 입력해주세요.")
        except ValueError:
            print("숫자를 입력해주세요.")
    
    # 5단계: 제출물 조회
    submissions = get_student_submissions(course_id, coursework_id)
    
    if submissions:
        # 6단계: JSON 파일로 저장 여부 확인
        save_choice = input("\n💾 결과를 JSON 파일로 저장하시겠습니까? (y/n): ").lower()
        if save_choice == 'y':
            save_submissions_to_json(course_id, coursework_id)

if __name__ == "__main__":
    try:
        interactive_mode()
    except KeyboardInterrupt:
        print("\n\n👋 프로그램을 종료합니다.")
    except Exception as error:
        print(f"\n❌ 오류가 발생했습니다: {error}")