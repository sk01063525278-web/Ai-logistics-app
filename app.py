import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="대한전선 AI 물류관리", layout="wide")

st.title("📦 AI 기반 대한전선 물류관리 시스템")
st.markdown("### 재고 + 일정 기반 리스크를 동시에 분석하는 스마트 물류 에이전트")
st.info("🤖 AI가 재고 및 생산/검사/포장 일정을 분석하여 납기 리스크를 예측합니다.")

uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 날짜 변환
    df['생산(입하)'] = pd.to_datetime(df['생산(입하)'])
    df['검사'] = pd.to_datetime(df['검사'])
    df['포장'] = pd.to_datetime(df['포장'])
    df['납기'] = pd.to_datetime(df['납기'])

    today = datetime.today()

    # 🔥 일정 리스크 분석
    def schedule_risk(row):
        days_left = (row['납기'] - row['생산(입하)']).days

        if days_left <= 7:
            return "🔴 위험/관리필요"
        elif days_left <= 14:
            return "🟡 주의/관리필요"
        else:
            return "🟢 정상"

    df['일정리스크'] = df.apply(schedule_risk, axis=1)

    st.subheader("📊 데이터 및 분석 결과")
    st.dataframe(df)

    # KPI
    위험 = (df['일정리스크'] == "🔴 위험/관리필요").sum()
    주의 = (df['일정리스크'] == "🟡 주의/관리필요").sum()
    정상 = (df['일정리스크'] == "🟢 정상").sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 위험", 위험)
    col2.metric("🟡 주의", 주의)
    col3.metric("🟢 정상", 정상)

    # 위험 필터
    st.subheader("⚠️ 일정 위험 품목")
    risk_df = df[df['일정리스크'] != "🟢 정상"]
    st.dataframe(risk_df)

    # 🔥 이미지 업로드 기능 (행 선택 기반)
    st.subheader("📸 품목 이미지 등록")

    item_list = df.index.tolist()
    selected_item = st.selectbox("품목 선택", item_list)

    uploaded_image = st.file_uploader("이미지 업로드", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        st.image(uploaded_image, caption=f"{selected_item}번 품목 이미지", width=300)

    # AI 코멘트
    st.subheader("🤖 AI 종합 분석")

    if 위험 > 0:
        st.error("납기 임박 또는 일정 여유 부족 품목 존재 → 긴급 관리 필요")
    elif 주의 > 0:
        st.warning("일부 품목 일정 여유 부족 → 관리 필요")
    else:
        st.success("전체 일정 안정 상태")

    st.info("권장 조치: 생산 일정 조정 또는 납기 재검토 필요")
