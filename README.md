⚡ 전국 충전기 설치현황 대시보드
Status License HTML5 JavaScript

전국 전기차 충전소 설치 현황을 실시간으로 시각화하는 인터랙티브 웹 대시보드입니다. 지도 기반 시각화, 다중 필터링, 통계 분석, 엑셀 다운로드 기능을 통해 충전 인프라를 직관적으로 분석할 수 있습니다.

🚀 라이브 데모 보기
👆 GitHub Pages 배포 후 위 링크를 실제 URL로 수정하세요!

✨ 주요 기능
🗺️ 지도 기반 시각화
Leaflet + MarkerCluster를 활용한 전국 충전소 위치 표시
네모 마커로 각 사이트별 충전기 개수 표시
8가지 색상 구분: 만료, 1개월, 3개월, 6개월, 26하반기, 27상반기, 27하반기, 기타
상세 팝업: 사이트ID, 충전소명, 주소, 계약기간 + 네이버 지도 연동
🔍 강력한 검색 & 필터링
실시간 검색: 충전소명, 주소, 사이트ID로 즉시 검색
다중 선택 필터: 구분, 모델분류 복수 선택 가능
권역 필터: 단일 선택 드롭다운
🎯 27년만료 대상충전기: 원클릭 특별 필터
📊 실시간 통계 대시보드
현황 통계: 총 사이트/충전기 수 + 현재 표시 중인 데이터 수
3가지 막대 그래프: 구분별, 모델분류별, 권역별 분포
⭐ 내림차순 정렬: 숫자가 가장 큰 항목이 왼쪽에 표시
📥 데이터 관리
엑셀 다운로드: 필터링된 결과를 즉시 Excel 파일로 저장
JSON 데이터 분리: 대용량 엑셀을 가벼운 JSON으로 최적화
자동 파일명: 날짜와 검색어 포함 (예: 충전소목록_20260326.xlsx)
🛠️ 기술 스택
분류	기술/라이브러리	버전	용도
Frontend	HTML5, CSS3, JavaScript	ES6+	메인 UI/UX
지도	Leaflet.js	1.9.4	지도 렌더링
클러스터링	Leaflet.markercluster	1.5.3	마커 클러스터링
차트	Chart.js	4.4.0	통계 그래프
엑셀	SheetJS	0.18.5	Excel 다운로드
데이터 처리	Python + Pandas	3.x	엑셀 → JSON 변환
📁 프로젝트 구조
📦 ev-charging-dashboard/
├── 📄 index.html                    # 메인 대시보드 (UI + JavaScript)
├── 📊 charging_data.json            # 충전소 데이터 (JSON 형식)
├── 🐍 create_dashboard.py           # Python 데이터 생성 스크립트
├── 📋 README.md                     # 프로젝트 문서
└── 📁 원본데이터/
    └── 충전기_상태정보_리스트_YYYYMMDD_모델명권역기입.xlsx
파일 설명
index.html: 전체 대시보드 UI 및 JavaScript 로직 포함
charging_data.json: 사이트 단위로 집계된 충전소 데이터
create_dashboard.py: 엑셀 파일을 읽어서 JSON과 HTML을 생성하는 스크립트
💻 설치 및 실행
⚠️ 중요: JSON 데이터를 외부에서 로드하므로 반드시 웹 서버 환경에서 실행해야 합니다.
HTML 파일을 직접 더블클릭하면 CORS 에러로 데이터가 로드되지 않습니다.

방법 1: Python 웹 서버 (추천)
Copy# 1. 저장소 클론 또는 파일 다운로드
git clone https://github.com/your-username/ev-charging-dashboard.git
cd ev-charging-dashboard

# 2. Python 웹 서버 실행
python -m http.server 8000

# 3. 브라우저에서 접속
# http://localhost:8000
방법 2: VS Code Live Server
VS Code에서 프로젝트 폴더 열기
Live Server 확장프로그램 설치
index.html 우클릭 → "Open with Live Server"
방법 3: 기타 웹 서버
Copy# Node.js http-server
npm install -g http-server
http-server -p 8000

# PHP 내장 서버
php -S localhost:8000
🌐 GitHub Pages 배포
단계별 배포 가이드
GitHub 저장소 생성

새 public 저장소 생성 (예: ev-charging-dashboard)
파일 업로드

Copygit add index.html charging_data.json README.md
git commit -m "Initial commit: Add charging dashboard"
git push origin main
GitHub Pages 활성화

저장소 → Settings → Pages
Source: Deploy from a branch
Branch: main / Folder: / (root)
Save 클릭
접속

1-5분 후 https://your-username.github.io/your-repository-name/ 접속 가능
🔄 데이터 업데이트
새로운 엑셀 데이터로 대시보드를 갱신하는 방법입니다.

1단계: 엑셀 파일 교체
Copy# 새 엑셀 파일을 프로젝트 폴더에 배치
충전기_상태정보_리스트_20260326_모델명권역기입.xlsx
2단계: Python 스크립트 실행
Copy# create_dashboard.py에서 파일명 확인 후 실행
python create_dashboard.py

# 출력 예시:
# ✅ 데이터 로드 완료: 15,234행
# ✅ JSON 데이터 저장: charging_data.json
# 🎉 완료!
3단계: GitHub 업데이트
Copygit add charging_data.json
git commit -m "Update charging data - 2026-03-26"
git push origin main
자동 반영: GitHub Pages는 푸시 후 1-5분 내에 자동으로 업데이트됩니다.

🎯 사용 가이드
기본 사용법
필터링

상단 헤더에서 원하는 조건 선택
🏢 구분: 복수 선택 가능 (투자/환경 기간별)
🔧 모델분류: 복수 선택 가능 (우선순위 정렬)
🌏 권역: 단일 선택
검색

좌측 검색창에 키워드 입력 (실시간 검색)
Enter 키 또는 🔍 버튼으로 지도 자동 이동
데이터 다운로드

원하는 조건으로 필터링 후
📥 엑셀 다운로드 버튼 클릭
고급 기능
네이버 지도 연동

마커 클릭 → 팝업 → "🗺️ 네이버 지도에서 검색" 버튼
충전소 목록에서 지도 이동

좌측 목록 항목 클릭 → 해당 위치로 자동 이동
🐛 문제 해결
자주 발생하는 문제
❌ 데이터가 로드되지 않음

해결방법:
1. charging_data.json 파일이 index.html과 같은 폴더에 있는지 확인
2. 웹 서버로 실행했는지 확인 (직접 더블클릭 ❌)
3. 브라우저 콘솔(F12)에서 에러 메시지 확인
❌ 지도가 표시되지 않음

해결방법:
1. 인터넷 연결 확인
2. 방화벽/광고 차단기 비활성화
3. 다른 브라우저로 시도 (Chrome, Firefox 권장)
❌ 엑셀 다운로드 실패

해결방법:
1. 브라우저 팝업 차단 해제
2. 다운로드 권한 허용
3. 페이지 새로고침 후 재시도
브라우저 호환성
브라우저	지원 버전	상태
Chrome	90+	✅ 완벽 지원
Firefox	88+	✅ 완벽 지원
Safari	14+	✅ 완벽 지원
Edge	90+	✅ 완벽 지원
IE 11	-	❌ 지원 안 함
🎨 색상 가이드
구분	색상	설명
만료	🔴 #E74C3C	계약 만료된 충전소
1개월	🟠 #FF8C42	1개월 이내 만료 예정
3개월	🟡 #F39C12	3개월 이내 만료 예정
6개월	🟢 #27AE60	6개월 이내 만료 예정
26하반기	🔵 #17A2B8	2026년 하반기 만료
27상반기	🔵 #007BFF	2027년 상반기 만료
27하반기	🟣 #6F42C1	2027년 하반기 만료
구분없음	⚪ #ADB5BD	구분값이 없는 경우
🤝 기여하기
Fork 저장소
Feature 브랜치 생성 (git checkout -b feature/amazing-feature)
변경사항 커밋 (git commit -m 'Add amazing feature')
브랜치에 Push (git push origin feature/amazing-feature)
Pull Request 생성
📄 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

MIT License - 자유롭게 사용, 수정, 배포 가능
📞 문의 및 지원
이슈 등록: GitHub Issues
이메일: your.email@example.com
🙏 감사의 말
이 프로젝트는 다음 오픈소스 라이브러리를 사용합니다:

Leaflet - 지도 라이브러리
Chart.js - 차트 라이브러리
SheetJS - Excel 파일 처리
OpenStreetMap - 지도 데이터
⚡ 전국 충전기 설치현황 대시보드

Made with ❤️ for EV Infrastructure Analysis
