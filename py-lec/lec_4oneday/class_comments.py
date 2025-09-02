import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

# OAuth 2.0 scope - 댓글 읽기를 위한 추가 권한
SCOPES = [
    'https://www.googleapis.com/auth/classroom.announcements.readonly',
    'https://www.googleapis.com/auth/classroom.courses.readonly', 
    'https://www.googleapis.com/auth/classroom.student-submissions.students.readonly'
]

# 설정값들
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

def get_classroom_service():
    """인증된 Classroom API 서비스 객체 반환"""
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('classroom', 'v1', credentials=creds)
    return service

def list_courses():
    """코스 목록 조회"""
    try:
        service = get_classroom_service()
        results = service.courses().list(pageSize=50).execute()
        courses = results.get('courses', [])
        
        if not courses:
            print('코스를 찾을 수 없습니다.')
            return []
        
        print('사용 가능한 코스들:')
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course.get('name', '이름 없음')} (ID: {course.get('id')})")
        
        return courses
        
    except Exception as error:
        print(f'코스 조회 중 오류 발생: {error}')
        return []

def get_assignment_comments(course_id):
    """코스의 모든 과제(Assignment) 댓글 가져오기"""
    service = get_classroom_service()
    all_comments = []
    
    try:
        # CourseWork(과제) 목록 조회
        print("과제 목록 조회 중...")
        coursework_response = service.courses().courseWork().list(courseId=course_id).execute()
        
        coursework_list = coursework_response.get('courseWork', [])
        print(f"총 {len(coursework_list)}개의 과제 발견")
        
        for coursework in coursework_list:
            coursework_id = coursework['id']
            coursework_title = coursework.get('title', '')
            
            print(f"과제 '{coursework_title}' 댓글 수집 중...")
            
            # 각 과제의 학생 제출물들 조회
            try:
                submissions_response = service.courses().courseWork().studentSubmissions().list(
                    courseId=course_id,
                    courseWorkId=coursework_id
                ).execute()
                
                submissions = submissions_response.get('studentSubmissions', [])
                
                for submission in submissions:
                    submission_id = submission['id']
                    student_id = submission.get('userId', '')
                    
                    try:
                        # 제출물의 댓글들 조회
                        comments_response = service.courses().courseWork().studentSubmissions().comments().list(
                            courseId=course_id,
                            courseWorkId=coursework_id,
                            submissionId=submission_id
                        ).execute()
                        
                        comments = comments_response.get('comments', [])
                        
                        for comment in comments:
                            comment_data = {
                                'coursework_id': coursework_id,
                                'coursework_title': coursework_title,
                                'submission_id': submission_id,
                                'student_id': student_id,
                                'comment_id': comment['id'],
                                'author_id': comment.get('authorId', ''),
                                'text': comment.get('text', ''),
                                'creation_time': comment.get('creationTime', '')
                            }
                            all_comments.append(comment_data)
                            
                    except Exception as e:
                        # 댓글이 없는 제출물은 건너뛰기
                        continue
                        
            except Exception as e:
                print(f"과제 '{coursework_title}' 처리 중 오류: {e}")
                continue
    
    except Exception as error:
        print(f'과제 댓글 조회 중 오류 발생: {error}')
    
    return all_comments

def main():
    print("Google Classroom Comments Reader")
    print("=" * 40)
    
    # 코스 목록 조회
    courses = list_courses()
    if not courses:
        return
    
    # 코스 선택
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
                print(f"\n선택된 코스: {course_name}")
                break
            else:
                print("올바른 번호를 입력해주세요.")
        except ValueError:
            print("숫자를 입력해주세요.")
    
    # 댓글 수집
    print(f"\n코스 '{course_name}'의 모든 과제 댓글을 수집합니다...")
    comments = get_assignment_comments(course_id)
    
    if comments:
        # JSON 파일로 저장
        filename = f"classroom_comments_{course_id}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
        
        print(f"\n총 {len(comments)}개의 과제 댓글을 '{filename}' 파일로 저장했습니다.")
        
        # 과제별 댓글 통계
        coursework_stats = {}
        for comment in comments:
            title = comment['coursework_title']
            coursework_stats[title] = coursework_stats.get(title, 0) + 1
        
        print("\n과제별 댓글 수:")
        for title, count in coursework_stats.items():
            print(f"- {title}: {count}개")
    else:
        print("과제 댓글을 찾을 수 없습니다.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    except Exception as error:
        print(f"오류가 발생했습니다: {error}")