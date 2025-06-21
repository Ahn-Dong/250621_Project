import pandas as pd
import streamlit as st
from collections import Counter
import re

# 페이지 설정
st.set_page_config(page_title="서울시 맛집 찾기 (by 세금)", layout="wide")
st.title("🍽️ 서울시 맛집 찾기 (by 세금)")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 문자열 정제 및 필터링 함수
    def extract_valid_names(text):
        if pd.isna(text):
            return []
        
        # 정규식으로 괄호 포함된 항목 또는 숫자형 리스트 제거 예: '1)', '②', '(주)' 등
        cleaned = re.sub(r"[\d]+[\)\.]|[①-⑩⑴-⑽]|[\(\[].*?[\)\]]", "", str(text))
        
        # 한글/영문/숫자/공백만 남기고 나머지 제거
        candidates = re.findall(r"[가-힣A-Za-z0-9&() ]{2,}", cleaned)
        
        # 필터: 한글 3글자 이상 or 영문/숫자 1단어 이상
        filtered = []
        for name in candidates:
            name_strip = name.strip()
            if len(re.findall(r"[가-힣]", name_strip)) >= 3:
                filtered.append(name_strip)
            elif len(re.findall(r"[A-Za-z0-9]", name_strip)) >= 3:
                filtered.append(name_strip)
        return
