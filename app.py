import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components
import os
from pathlib import Path

# ⭐ Streamlit 페이지 설정
st.set_page_config(
    page_title="전국 충전기 설치현황", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ⭐ 엑셀 데이터 처리 함수
@st.cache_data
def process_excel_data(file_buffer):
    """엑셀 파일을 읽어서 사이트 데이터로 변환"""
    try:
        df = pd.read_excel(file_buffer, header=3)
        df_filtered = df.dropna(subset=['X좌표', 'Y좌표'])
        site_data = {}
        
        for idx, row in df_filtered.iterrows():
            site_id_raw = row['사이트ID']
            if pd.isna(site_id_raw): 
                continue
            
            site_id = str(int(float(site_id_raw))) if isinstance(site_id_raw, (int, float)) else str(site_id_raw)
            
            if site_id not in site_data:
                site_data[site_id] = {
                    'site_id': site_id,
                    'station_id': str(row['충전소ID']) if pd.notna(row['충전소ID']) else '',
                    'station_name': str(row['충전소명']) if pd.notna(row['충전소명']) else '',
                    'address': str(row['주소1']) if pd.notna(row['주소1']) else '',
                    'model_class': str(row['모델분류(자동)']) if pd.notna(row['모델분류(자동)']) and str(row['모델분류(자동)']) != 'nan' else '미분류',
                    'region': str(row['권역']) if pd.notna(row['권역']) and str(row['권역']) != 'nan' else '기타',
                    'category': str(row['구분']) if pd.notna(row['구분']) and str(row['구분']) != 'nan' else '',
                    'contract_start': str(row['운영계약 시작일']).split(' ')[0] if pd.notna(row['운영계약 시작일']) else '',
                    'contract_end': str(row['운영계약 종료일']).split(' ')[0] if pd.notna(row['운영계약 종료일']) else '',
                    'longitude': float(row['X좌표']),
                    'latitude': float(row['Y좌표']),
                    'charger_count': 0
                }
            site_data[site_id]['charger_count'] += 1
            
        return list(site_data.values())
        
    except Exception as e:
        st.error(f"❌ 데이터 처리 중 오류 발생: {e}")
        return []

# ⭐ HTML 템플릿 로드 및 데이터 주입
def render_dashboard_with_data(json_data_list):
    """기존 HTML에 새로운 데이터를 주입하여 렌더링"""
    
    # 기존 index.html 파일 읽기
    html_file = Path('index.html')
    if not html_file.exists():
        st.error("❌ 'index.html' 파일을 찾을 수 없습니다. 같은 폴더에 있는지 확인해주세요.")
        st.info("💡 기존에 만든 HTML 대시보드 파일이 필요합니다.")
        return
    
    try:
        html_content = html_file.read_text(encoding='utf-8')
    except Exception as e:
        st.error(f"❌ HTML 파일 읽기 실패: {e}")
        return
    
    # JSON 데이터 문자열로 변환
    json_data_str = json.dumps(json_data_list, ensure_ascii=False)
    
    # ⭐ CORS 문제 해결: fetch() 코드를 직접 데이터 주입으로 대체
    modified_html = html_content.replace(
        "const response = await fetch('charging_data.json');", 
        "// 데이터를 직접 주입하므로 fetch 불필요"
    ).replace(
        "if (!response.ok) {", 
        "if (false) {"  # 에러 블록 비활성화
    ).replace(
        "throw new Error('데이터 파일을 찾을 수 없습니다.');", 
        ""
    ).replace(
        "allSites = await response.json();", 
        f"allSites = {json_data_str};"
    ).replace(
        "document.getElementById('loadingOverlay').style.display = 'none';",
        "document.getElementById('loadingOverlay').style.display = 'none'; console.log('✅ Streamlit에서 데이터 로드 완료:', allSites.length + '개 사이트');"
    )
    
    # Streamlit 컴포넌트로 렌더링
    components.html(
        modified_html, 
        height=900, 
        scrolling=True
    )

# ==========================================
# 🎈 Streamlit UI 메인 구성
# ==========================================

st.title("⚡ 전국 충전기 설치현황 (Streamlit 연동)")

# 사이드바 구성
with st.sidebar:
    st.header("📁 데이터 관리")
    
    # 파일 업로드
    uploaded_file = st.file_uploader(
        "새로운 충전기 엑셀 파일 업로드", 
        type=['xlsx', 'xls'],
        help="업로드하지 않으면 기존 데이터를 사용합니다."
    )
    
    st.markdown("---")
    
    # 기존 데이터 정보
    if os.path.exists('charging_data.json'):
        with open('charging_data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        
        st.info(f"💾 기존 데이터: {len(existing_data):,}개 사이트")
        
        if st.button("🔄 기존 데이터로 새로고침"):
            st.rerun()
    else:
        st.warning("⚠️ 기존 'charging_data.json' 파일이 없습니다.")
    
    st.markdown("---")
    st.markdown("### 📋 사용법")
    st.markdown("""
    1. **엑셀 업로드**: 새로운 데이터 즉시 반영
    2. **기존 HTML**: 디자인 100% 보존
    3. **실시간 업데이트**: 파일 변경시 자동 갱신
    """)

# 메인 로직
if uploaded_file is not None:
    # 새 엑셀 파일 업로드된 경우
    with st.spinner('📊 엑셀 데이터를 분석하고 대시보드를 업데이트하는 중...'):
        new_data = process_excel_data(uploaded_file)
        
        if new_data:
            total_chargers = sum(site['charger_count'] for site in new_data)
            st.success(f"✅ 업데이트 완료! 사이트 {len(new_data):,}개, 충전기 {total_chargers:,}기")
            
            # 새 데이터로 대시보드 렌더링
            render_dashboard_with_data(new_data)
        else:
            st.error("❌ 데이터 처리에 실패했습니다.")
else:
    # 기존 데이터 사용
    if os.path.exists('charging_data.json'):
        try:
            with open('charging_data.json', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            
            total_chargers = sum(site['charger_count'] for site in existing_data)
            st.info(f"📊 현재 데이터: 사이트 {len(existing_data):,}개, 충전기 {total_chargers:,}기")
            
            render_dashboard_with_data(existing_data)
            
        except Exception as e:
            st.error(f"❌ 기존 데이터 로드 실패: {e}")
    else:
        # 초기 상태 - 안내 메시지
        st.markdown("""
        ## 🚀 시작하기
        
        왼쪽 사이드바에서 **충전기 엑셀 파일을 업로드**하거나, 
        기존 `charging_data.json` 파일이 있다면 자동으로 로드됩니다.
        
        ### 📁 필요한 파일들
        - `index.html` - 기존에 만든 대시보드 HTML 파일
        - `charging_data.json` - 기존 데이터 (선택사항)
        - 엑셀 파일 - 새로운 데이터 업로드용
        
        ### ✨ 장점
        - 🎨 **기존 디자인 100% 보존**
        - 📁 **실시간 파일 업로드**
        - 🔄 **즉시 업데이트**
        - 🌐 **웹 배포 가능**
        """)
