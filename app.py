import streamlit as st
import json
import streamlit.components.v1 as components
from pathlib import Path

# ⭐ 페이지 설정 - 전체 화면 모드
st.set_page_config(
    page_title="전국 충전기 설치현황", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ⭐ 모든 Streamlit UI 요소 완전 제거 + 진정한 전체화면 CSS
st.markdown("""
<style>
    /* Streamlit 기본 요소들 완전 숨김 */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* 사이드바 완전 제거 */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* 메인 컨테이너 여백 완전 제거 */
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* 전체 앱 여백 제거 */
    .stApp {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* iframe을 진정한 전체화면으로 */
    iframe {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        z-index: 999999 !important;
    }
    
    /* 스크롤바 숨김 (선택사항) */
    body {
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ⭐ HTML 대시보드 렌더링 함수
def render_fullscreen_dashboard():
    """index.html을 전체화면으로 렌더링"""
    
    html_file = Path('index.html')
    json_file = Path('charging_data.json')
    
    # 파일 존재 확인
    if not html_file.exists():
        st.error("❌ 'index.html' 파일을 찾을 수 없습니다.")
        st.stop()
    
    if not json_file.exists():
        st.error("❌ 'charging_data.json' 파일을 찾을 수 없습니다.")
        st.stop()
    
    try:
        # HTML 파일 읽기
        html_content = html_file.read_text(encoding='utf-8')
        
        # JSON 데이터 읽기
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # JSON을 JavaScript 문자열로 변환
        json_data_str = json.dumps(json_data, ensure_ascii=False)
        
        # ⭐ CORS 문제 해결: fetch를 직접 데이터 주입으로 대체
        modified_html = html_content.replace(
            "const response = await fetch('charging_data.json');", 
            "// Streamlit에서 데이터 직접 주입"
        ).replace(
            "if (!response.ok) {", 
            "if (false) {"
        ).replace(
            "throw new Error('데이터 파일을 찾을 수 없습니다.');", 
            ""
        ).replace(
            "allSites = await response.json();", 
            f"allSites = {json_data_str};"
        ).replace(
            "document.getElementById('loadingOverlay').style.display = 'none';",
            """
            document.getElementById('loadingOverlay').style.display = 'none';
            console.log('✅ Streamlit에서 데이터 로드 완료:', allSites.length + '개 사이트');
            """
        )
        
        # ⭐ 전체화면 렌더링 (CSS가 실제 크기 제어)
        components.html(
            modified_html, 
            height=1200,  # CSS의 100vh가 우선 적용됨
            scrolling=False
        )
        
    except Exception as e:
        st.error(f"❌ 파일 처리 중 오류: {e}")

# ⭐ 메인 실행
render_fullscreen_dashboard()
