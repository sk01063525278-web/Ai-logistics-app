import streamlit as st
import pandas as pd

st.set_page_config(page_title="대한전선 AI 물류관리", layout="wide")

st.title("📦 대한전선 AI 물류관리 시스템")

uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📊 원본 데이터")
    st.dataframe(df)

    # 분석 함수
    def analyze(row):
        stock = row['현재재고']
        min_stock = row['최소재고']
        incoming = row['입고예정']
        outgoing = row['출고예정']

        status = "정상"
        risk = "정상"

        if stock < min_stock:
            status = "부족"

        if stock + incoming - outgoing < 0:
            risk = "납기 위험"

        return pd.Series([status, risk])

    df[['재고상태', '납기리스크']] = df.apply(analyze, axis=1)

    st.subheader("📈 분석 결과")
    st.dataframe(df)

    # 요약 KPI
    부족 = (df['재고상태'] == '부족').sum()
    정상 = (df['재고상태'] == '정상').sum()
    위험 = (df['납기리스크'] == '납기 위험').sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("⚠️ 부족 자재", 부족)
    col2.metric("✅ 정상 자재", 정상)
    col3.metric("🚨 납기 위험", 위험)

    # 위험 자재 필터
    st.subheader("⚠️ 위험 자재만 보기")
    risk_df = df[(df['재고상태'] == '부족') | (df['납기리스크'] == '납기 위험')]
    st.dataframe(risk_df)

    # AI 코멘트 (간단 버전)
    st.subheader("🤖 AI 분석 코멘트")

    if 부족 > 0:
        st.warning("현재 다수 자재가 최소재고 이하 상태입니다.")
    if 위험 > 0:
        st.error("납기 지연 가능성이 있는 자재가 존재합니다.")
    if 부족 == 0 and 위험 == 0:
        st.success("현재 물류 상태는 안정적입니다.")

    st.info("권장 조치: 부족 자재 긴급 발주 및 출고 우선순위 조정 필요")