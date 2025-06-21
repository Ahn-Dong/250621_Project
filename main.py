import pandas as pd
import streamlit as st
from collections import Counter
import re

st.set_page_config(page_title="서울시 중구 맛집 찾기", layout="wide")
st.title("🍽️ 서울시 중구 맛집 찾기")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    def extract_restaurant_names(text):
        if pd.isna(text):
            return []
        return re.findall(r"[가-힣A-Za-z0-9&() ]{2,}", text)

    all_places = []
    for place in df['집행장소']:
        names = extract_restaurant_names(place)
        all_places.extend(names)

    counter = Counter(all_places)
    most_common = counter.most_common(30)

    st.subheader("📊 빈도순 맛집 리스트 (상위 30개)")
    if most_common:
        result_df = pd.DataFrame(most_common, columns=["식당 이름", "등장 횟수"])
        st.dataframe(result_df, use_container_width=True)
    else:
        st.write("❌ 식당 정보를 찾을 수 없습니다.")
    
    st.markdown("---")
    st.markdown("🔜 *추후 서울시 모든 구로 확대 예정입니다.*")

else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
