import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# OAuth 2.0 scope - Classroom API 접근 권한 (최소 권한으로 시작)
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.students.readonly',
    'https://www.googleapis.com/auth/classroom.announcements.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.students.readonly'
]

# 설정값들 - 실제 값으로 변경 필요
CREDENTIALS_FILE = 'credentials.json'  # Google Cloud에서 다운로드한 JSON 파일 경로
TOKEN_FILE = 'token.pickle'  # 토큰 저장 파일명

def get_credentials():
    """OAuth 2.0 인증을 통해 credentials 객체 반환"""
    creds = None
    
    # 기존에 저장된 토큰이 있는지 확인
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # 유효하지 않거나 만료된 토큰인 경우
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 토큰 갱신 시도
            creds.refresh(Request())
        else:
            # 새로운 인증 플로우 시작
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)  # 설정한 credentials 파일 사용
            creds = flow.run_local_server(port=0)
        
        # 토큰을 파일에 저장하여 다음번에 재사용
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_classroom_service():
    """인증된 Classroom API 서비스 객체 반환"""
    credentials = get_credentials()
    service = build('classroom', 'v1', credentials=credentials)
    return service

def test_authentication():
    """인증이 제대로 되었는지 테스트"""
    try:
        service = get_classroom_service()
        
        # 사용자의 코스 목록 조회로 테스트
        results = service.courses().list(pageSize=10).execute()
        courses = results.get('courses', [])
        
        if not courses:
            print('No courses found.')
        else:
            print('Courses:')
            for course in courses:
                print(f"- {course['name']} (ID: {course['id']})")
        
        return service
        
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def get_student_submissions(course_id, coursework_id):
    """특정 과제의 학생 제출물들을 가져오는 예시"""
    try:
        service = get_classroom_service()
        
        # 학생 제출물 목록 조회
        submissions = service.courses().courseWork().studentSubmissions().list(
            courseId=course_id,
            courseWorkId=coursework_id,
            pageSize=100
        ).execute().get('studentSubmissions', [])
        
        print(f"Found {len(submissions)} submissions:")
        
        for submission in submissions:
            student_id = submission.get('userId')
            state = submission.get('state', 'UNKNOWN')
            
            # 제출 시간
            creation_time = submission.get('creationTime', 'Not available')
            
            # 점수 (있는 경우)
            assigned_grade = submission.get('assignedGrade', 'Not graded')
            
            print(f"Student ID: {student_id}")
            print(f"State: {state}")
            print(f"Creation Time: {creation_time}")
            print(f"Grade: {assigned_grade}")
            
            # 첨부 파일들
            attachments = submission.get('assignmentSubmission', {}).get('attachments', [])
            if attachments:
                print("Attachments:")
                for attachment in attachments:
                    if 'driveFile' in attachment:
                        file_info = attachment['driveFile']
                        print(f"  - Drive File: {file_info.get('title', 'Unknown')}")
                    elif 'link' in attachment:
                        print(f"  - Link: {attachment['link'].get('url', 'Unknown')}")
            
            print("-" * 50)
            
        return submissions
        
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

if __name__ == "__main__":
    print("Google Classroom OAuth 2.0 Authentication Test")
    print("=" * 50)
    
    # 인증 테스트
    service = test_authentication()
    
    if service:
        print("\n✅ Authentication successful!")
        print("\nYou can now use the Classroom API.")
        
        # 사용 예시 - 실제 값으로 변경 필요
        print("\n📝 사용 예시:")
        print("실제 Course ID와 Coursework ID를 얻으려면:")
        print("1. courses 목록에서 원하는 코스의 ID 확인")
        print("2. 해당 코스의 과제 목록 조회")
        
        # 실제 사용 시 아래 주석을 해제하고 실제 ID로 변경
        # course_id = "실제_코스_ID"  # 예: "123456789"
        # coursework_id = "실제_과제_ID"  # 예: "987654321" 
        # get_student_submissions(course_id, coursework_id)
    else:
        print("\n❌ Authentication failed!")