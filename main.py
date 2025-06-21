import pandas as pd
import streamlit as st
from collections import Counter
import re

# 페이지 설정
st.set_page_config(page_title="서울시 맛집 찾기 (by 세금)", layout="wide")
st.title("🍽️ 서울시 맛집 찾기 (by 세금)")

# 설명 영역
with st.expander("ℹ️ 이 웹앱은 무엇인가요?", expanded=True):
    st.markdown("""
    ### 👀 어떤 기준으로 맛집을 찾나요?
    이 웹앱은 **서울시 본청 업무추진비 집행내역** 데이터를 활용해,
    공공기관 관계자들이 **자주 방문한 식당**을 빈도순으로 정리합니다.

    > **가정:** 공공기관에서 자주 방문한 곳은 그만큼 품질이 검증되었을 가능성이 높다 → **맛집일 가능성**이 있다!

    ---
    ### 📁 어떤 파일을 업로드해야 하나요?
    - [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/OA-27391/S/1/datasetView.do)에서 내려받은 CSV 파일을 업로드해주세요.
    - 보통 이름은 `서울시 본청 업무추진비 목록.csv` 혹은 `서울시 본청 업무추진비 목록2.csv` 등으로 되어 있습니다.
    - 파일은 반드시 **CSV 형식**이어야 하며, **`집행장소` 열이 포함되어야** 합니다.

    ---
    """)

# 파일 업로드
uploaded_file = st.file_uploader("📤 CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except Exception as e:
        st.error(f"파일을 읽는 도중 문제가 발생했습니다: {e}")
    else:
        def extract_valid_names(text):
            if pd.isna(text):
                return []
            cleaned = re.sub(r"[\d]+[\)\.]|[①-⑩⑴-⑽]|[\(\[].*?[\)\]]", "", str(text))
            candidates = re.findall(r"[가-힣A-Za-z0-9&() ]{2,}", cleaned)
            filtered = []
            for name in candidates:
                name_strip = name.strip()
                if len(re.findall(r"[가-힣]", name_strip)) >= 2:
                    filtered.append(name_strip)
                elif len(re.findall(r"[A-Za-z0-9]", name_strip)) >= 2:
                    filtered.append(name_strip)
            return filtered

        all_places = []
        for place in df['집행장소']:
            all_places.extend(extract_valid_names(place))

        counter = Counter(all_places)
        most_common = counter.most_common(30)

        st.subheader("📊 등장 빈도 기반 맛집 순위 (Top 30)")
        if most_common:
            result_df = pd.DataFrame(most_common, columns=["식당 이름", "등장 횟수"])
            st.dataframe(result_df, use_container_width=True)
        else:
            st.warning("😥 식당 이름이 감지되지 않았습니다. CSV 내용을 확인하거나 정제 조건을 수정해주세요.")
else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
