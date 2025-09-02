# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
import os
import pickle
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from urllib.parse import urlparse
import re

# OAuth 2.0 scope - 파일 다운로드를 위한 권한
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.students.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

# 설정값들
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'
DOWNLOAD_DIR = 'downloaded_files'

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
    drive_service = build('drive', 'v3', credentials=creds)
    return service, drive_service

def list_courses():
    """코스 목록 조회"""
    try:
        service, _ = get_classroom_service()
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

def sanitize_filename(filename):
    """파일명에서 특수문자 제거"""
    # 윈도우/리눅스에서 사용할 수 없는 문자들 제거
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized.strip()

def download_file_from_drive(drive_service, file_id, filename, download_path):
    """Google Drive에서 파일 다운로드"""
    try:
        # 파일 메타데이터 가져오기
        file_metadata = drive_service.files().get(fileId=file_id).execute()
        file_name = file_metadata.get('name', filename)
        
        # 파일 다운로드
        request = drive_service.files().get_media(fileId=file_id)
        
        safe_filename = sanitize_filename(file_name)
        full_path = os.path.join(download_path, safe_filename)
        
        # 같은 이름의 파일이 있으면 번호 추가
        counter = 1
        original_path = full_path
        while os.path.exists(full_path):
            name, ext = os.path.splitext(original_path)
            full_path = f"{name}_{counter}{ext}"
            counter += 1
        
        with open(full_path, 'wb') as f:
            downloader = request.execute()
            f.write(downloader)
        
        print(f"    파일 다운로드 완료: {safe_filename}")
        return True, safe_filename
        
    except Exception as e:
        print(f"    파일 다운로드 실패 ({file_id}): {e}")
        return False, None

def get_assignment_attachments(course_id):
    """코스의 모든 과제 제출물 첨부파일 가져오기"""
    service, drive_service = get_classroom_service()
    all_attachments = []
    
    # 다운로드 디렉토리 생성
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    
    try:
        # CourseWork(과제) 목록 조회
        print("과제 목록 조회 중...")
        coursework_response = service.courses().courseWork().list(courseId=course_id).execute()
        
        coursework_list = coursework_response.get('courseWork', [])
        print(f"총 {len(coursework_list)}개의 과제 발견")
        
        for coursework in coursework_list:
            coursework_id = coursework['id']
            coursework_title = coursework.get('title', '제목없음')
            
            print(f"\n과제 '{coursework_title}' (ID: {coursework_id}) 처리 중...")
            
            # 과제별 다운로드 디렉토리 생성
            safe_title = sanitize_filename(coursework_title)
            assignment_dir = os.path.join(DOWNLOAD_DIR, f"{safe_title}_{coursework_id}")
            if not os.path.exists(assignment_dir):
                os.makedirs(assignment_dir)
            
            # 학생 제출물 조회
            submissions_response = service.courses().courseWork().studentSubmissions().list(
                courseId=course_id,
                courseWorkId=coursework_id
            ).execute()
            
            submissions = submissions_response.get('studentSubmissions', [])
            print(f"  제출물: {len(submissions)}개 발견")
            
            attachment_count = 0
            for submission in submissions:
                submission_id = submission['id']
                student_id = submission.get('userId', '')
                
                # 제출물의 첨부파일들 확인
                attachments = submission.get('assignmentSubmission', {}).get('attachments', [])
                
                if attachments:
                    print(f"  제출물 {submission_id}에서 {len(attachments)}개 첨부파일 발견")
                    
                    # 학생별 디렉토리 생성
                    student_dir = os.path.join(assignment_dir, f"student_{student_id}")
                    if not os.path.exists(student_dir):
                        os.makedirs(student_dir)
                    
                    for attachment in attachments:
                        attachment_info = {
                            'coursework_id': coursework_id,
                            'coursework_title': coursework_title,
                            'submission_id': submission_id,
                            'student_id': student_id,
                            'attachment_type': '',
                            'file_name': '',
                            'file_id': '',
                            'download_success': False,
                            'local_path': ''
                        }
                        
                        # Drive 파일 처리
                        if 'driveFile' in attachment:
                            drive_file = attachment['driveFile']
                            file_id = drive_file.get('id', '')
                            file_title = drive_file.get('title', '파일명없음')
                            
                            attachment_info.update({
                                'attachment_type': 'drive_file',
                                'file_name': file_title,
                                'file_id': file_id
                            })
                            
                            print(f"    Drive 파일: {file_title}")
                            success, downloaded_name = download_file_from_drive(
                                drive_service, file_id, file_title, student_dir
                            )
                            
                            if success:
                                attachment_info['download_success'] = True
                                attachment_info['local_path'] = os.path.join(student_dir, downloaded_name)
                                attachment_count += 1
                        
                        # YouTube 동영상 링크 처리
                        elif 'youTubeVideo' in attachment:
                            youtube_video = attachment['youTubeVideo']
                            video_id = youtube_video.get('id', '')
                            video_title = youtube_video.get('title', '동영상제목없음')
                            video_url = f"https://www.youtube.com/watch?v={video_id}"
                            
                            attachment_info.update({
                                'attachment_type': 'youtube_video',
                                'file_name': video_title,
                                'file_id': video_id,
                                'youtube_url': video_url
                            })
                            
                            print(f"    YouTube 동영상: {video_title} ({video_url})")
                            
                            # YouTube 링크는 텍스트 파일로 저장
                            link_filename = sanitize_filename(f"{video_title}_youtube_link.txt")
                            link_path = os.path.join(student_dir, link_filename)
                            
                            try:
                                with open(link_path, 'w', encoding='utf-8') as f:
                                    f.write(f"YouTube 동영상 링크\n")
                                    f.write(f"제목: {video_title}\n")
                                    f.write(f"URL: {video_url}\n")
                                    f.write(f"비디오 ID: {video_id}\n")
                                
                                attachment_info['download_success'] = True
                                attachment_info['local_path'] = link_path
                                attachment_count += 1
                                print(f"    YouTube 링크 저장 완료: {link_filename}")
                            except Exception as e:
                                print(f"    YouTube 링크 저장 실패: {e}")
                        
                        # 링크 처리
                        elif 'link' in attachment:
                            link_info = attachment['link']
                            link_url = link_info.get('url', '')
                            link_title = link_info.get('title', '링크제목없음')
                            
                            attachment_info.update({
                                'attachment_type': 'link',
                                'file_name': link_title,
                                'link_url': link_url
                            })
                            
                            print(f"    링크: {link_title} ({link_url})")
                            
                            # 링크를 텍스트 파일로 저장
                            link_filename = sanitize_filename(f"{link_title}_link.txt")
                            link_path = os.path.join(student_dir, link_filename)
                            
                            try:
                                with open(link_path, 'w', encoding='utf-8') as f:
                                    f.write(f"링크 정보\n")
                                    f.write(f"제목: {link_title}\n")
                                    f.write(f"URL: {link_url}\n")
                                
                                attachment_info['download_success'] = True
                                attachment_info['local_path'] = link_path
                                attachment_count += 1
                                print(f"    링크 저장 완료: {link_filename}")
                            except Exception as e:
                                print(f"    링크 저장 실패: {e}")
                        
                        all_attachments.append(attachment_info)
            
            print(f"  과제 '{coursework_title}' 첨부파일 총계: {attachment_count}개 다운로드")
    
    except Exception as error:
        print(f'첨부파일 조회 중 오류 발생: {error}')
    
    return all_attachments

def main():
    print("Google Classroom Assignment Files Downloader")
    print("=" * 50)
    
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
    
    # 첨부파일 수집 및 다운로드
    print(f"\n코스 '{course_name}'의 모든 과제 첨부파일을 다운로드합니다...")
    attachments = get_assignment_attachments(course_id)
    
    if attachments:
        # JSON 파일로 메타데이터 저장
        metadata_filename = f"attachment_metadata_{course_id}.json"
        with open(metadata_filename, 'w', encoding='utf-8') as f:
            json.dump(attachments, f, ensure_ascii=False, indent=2)
        
        # 통계 출력
        total_attachments = len(attachments)
        successful_downloads = sum(1 for att in attachments if att['download_success'])
        
        print(f"\n=== 다운로드 완료 ===")
        print(f"총 첨부파일: {total_attachments}개")
        print(f"성공적으로 다운로드: {successful_downloads}개")
        print(f"실패: {total_attachments - successful_downloads}개")
        print(f"메타데이터 저장: {metadata_filename}")
        print(f"파일 저장 위치: {DOWNLOAD_DIR}/")
        
        # 과제별 첨부파일 통계
        coursework_stats = {}
        for attachment in attachments:
            title = attachment['coursework_title']
            if title not in coursework_stats:
                coursework_stats[title] = {'total': 0, 'success': 0}
            coursework_stats[title]['total'] += 1
            if attachment['download_success']:
                coursework_stats[title]['success'] += 1
        
        print("\n과제별 첨부파일 다운로드 현황:")
        for title, stats in coursework_stats.items():
            print(f"- {title}: {stats['success']}/{stats['total']}개 성공")
            
        # 첨부파일 타입별 통계
        type_stats = {}
        for attachment in attachments:
            att_type = attachment['attachment_type']
            type_stats[att_type] = type_stats.get(att_type, 0) + 1
        
        print("\n첨부파일 타입별 통계:")
        for att_type, count in type_stats.items():
            print(f"- {att_type}: {count}개")
    else:
        print("첨부파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    except Exception as error:
        print(f"오류가 발생했습니다: {error}")