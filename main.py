import pandas as pd
import streamlit as st
from collections import Counter
import re

# 페이지 설정
st.set_page_config(page_title="서울시 맛집 찾기 (by 세금)", layout="wide")
st.title("🍽️ 서울시 맛집 찾기 (by 세금)")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except Exception as e:
        st.error(f"파일을 읽는 도중 문제가 발생했습니다: {e}")
    else:
        def extract_valid_names(text):
            if pd.isna(text):
                return []
            # 불필요한 패턴 제거
            cleaned = re.sub(r"[\d]+[\)\.]|[①-⑩⑴-⑽]|[\(\[].*?[\)\]]", "", str(text))
            # 한글/영문/숫자 패턴 추출
            candidates = re.findall(r"[가-힣A-Za-z0-9&() ]{2,}", cleaned)
            filtered = []
            for name in candidates:
                name_strip = name.strip()
                if len(re.findall(r"[가-힣]", name_strip)) >= 2:  # 한글 2자 이상
                    filtered.append(name_strip)
                elif len(re.findall(r"[A-Za-z0-9]", name_strip)) >= 2:  # 영/숫 2자 이상
                    filtered.append(name_strip)
            return filtered

        # 식당 이름 수집
        all_places = []
        for place in df['집행장소']:
            all_places.extend(extract_valid_names(place))

        counter = Counter(all_places)
        most_common = counter.most_common(30)

        st.subheader("📊 빈도순 맛집 리스트 (상위 30개)")
        if most_common:
            result_df = pd.DataFrame(most_common, columns=["식당 이름", "등장 횟수"])
            st.dataframe(result_df, use_container_width=True)
        else:
            st.warning("😥 식당 이름이 감지되지 않았습니다. 문자열 정제 조건을 완화해보거나 CSV 내용을 확인해주세요.")
else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
