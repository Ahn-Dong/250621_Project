import pandas as pd
import streamlit as st
from collections import Counter
import re

# 페이지 타이틀
st.set_page_config(page_title="서울시 중구 맛집 찾기", layout="wide")
st.title("🍽️ 서울시 중구 맛집 찾기")
st.caption("※ 집행장소 데이터를 기반으로 등장 빈도가 높은 식당을 맛집으로 간주합니다.")

# CSV 파일 로드
@st.cache_data
def load_data():
    df = pd.read_csv("서울시 본청 업무추진비 목록2.csv", encoding='utf-8')
    return df

df = load_data()

# '집행장소' 열에서 식당 이름 추출
def extract_restaurant_names(text):
    if pd.isna(text):
        return []
    # 한글이 포함된 문자열만 추출 (ex: '을지로골뱅이', '강남역 김밥천국')
    return re.findall(r"[가-힣A-Za-z0-9&() ]{2,}", text)

# 식당 이름 수집
all_places = []
for place in df['집행장소']:
    names = extract_restaurant_names(place)
    all_places.extend(names)

# 빈도수 계산
counter = Counter(all_places)
most_common = counter.most_common(30)

# 결과 출력
st.subheader("📊 빈도순 맛집 리스트 (상위 30개)")
if most_common:
    result_df = pd.DataFrame(most_common, columns=["식당 이름", "등장 횟수"])
    st.dataframe(result_df, use_container_width=True)
else:
    st.write("❌ 식당 정보를 찾을 수 없습니다. CSV 파일을 확인해주세요.")

# 추후 확장 안내
st.markdown("---")
st.markdown("🔜 *추후 서울시 모든 구로 확대 예정입니다.*")
