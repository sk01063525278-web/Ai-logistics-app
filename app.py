import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="대한전선 AI 물류관리", layout="wide")

st.title("📦 AI 기반 대한전선 물류관리 시스템")
st.markdown("### 재고 + 공정 일정 기반 리스크 분석")
st.info("🤖 생산 → 검사 → 포장 → 납기 공정을 고려한 AI 물류 분석 시스템")

uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 날짜 변환
    df['생산(입하)'] = pd.to_datetime(df['생산(입하)'])
    df['검사'] = pd.to_datetime(df['검사'])
    df['포장'] = pd.to_datetime(df['포장'])
    df['납기'] = pd.to_datetime(df['납기'])

    # 🔥 일정 리스크 계산 (수정된 기준)
    def schedule_risk(row):
        days_left = (row['납기'] - row['생산(입하)']).days

        if days_left <= 14:
            return "🔴 위험/관리필요"
        elif days_left <= 21:
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

    # 🔥 품목별 상세 + 이미지 업로드
    st.subheader("📦 품목별 공정 관리 및 사진 등록")

    for idx, row in df.iterrows():
        with st.expander(f"📦 품목 {idx} | 리스크: {row['일정리스크']}"):

            st.write("### 📅 공정 일정")
            st.write(f"생산(입하): {row['생산(입하)']}")
            st.write(f"검사: {row['검사']}")
            st.write(f"포장: {row['포장']}")
            st.write(f"납기: {row['납기']}")

            st.write("### 📸 공정별 사진 업로드")

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            with col1:
                prod_img = st.file_uploader(
                    f"생산(입하) 사진 업로드 - {idx}",
                    type=["png", "jpg", "jpeg"],
                    key=f"prod_{idx}"
                )
                if prod_img:
                    st.image(prod_img, width=200)

            with col2:
                insp_img = st.file_uploader(
                    f"검사 사진 업로드 - {idx}",
                    type=["png", "jpg", "jpeg"],
                    key=f"insp_{idx}"
                )
                if insp_img:
                    st.image(insp_img, width=200)

            with col3:
                pack_img = st.file_uploader(
                    f"포장 사진 업로드 - {idx}",
                    type=["png", "jpg", "jpeg"],
                    key=f"pack_{idx}"
                )
                if pack_img:
                    st.image(pack_img, width=200)

            with col4:
                del_img = st.file_uploader(
                    f"납기 사진 업로드 - {idx}",
                    type=["png", "jpg", "jpeg"],
                    key=f"del_{idx}"
                )
                if del_img:
                    st.image(del_img, width=200)

    # AI 코멘트
    st.subheader("🤖 AI 종합 분석")

    if 위험 > 0:
        st.error("납기 임박 품목 존재 → 긴급 대응 필요")
    elif 주의 > 0:
        st.warning("일정 여유 부족 품목 존재 → 관리 필요")
    else:
        st.success("전체 일정 안정 상태")

    st.info("권장 조치: 생산 일정 조정 또는 우선순위 재배치")
