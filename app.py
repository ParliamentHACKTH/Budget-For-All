import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from utils import mahalanobis_distance, remove_comma_and_convert_to_float, remove_comma_and_convert_to_int, remove_word_province

location_df = pd.read_csv("data/จังหวัด location.csv")
location_df = location_df.set_index("ชื่อจังหวัด")

# 0. งบที่จะได้รับ
budget_df = pd.read_csv("data/y68 Thailand's Budget per จังหวัด.tsv", sep="\t")
budget_df["ชื่อจังหวัด"] = budget_df["ชื่อจังหวัด"].apply(remove_word_province)
budget_df["งบประมาณ"] = budget_df["งบประมาณ"].apply(remove_comma_and_convert_to_int)
budget_df["งบประมาณ_adjusted"] = (budget_df["งบประมาณ"].values - budget_df["งบประมาณ"].values.mean()) / budget_df["งบประมาณ"].values.std()
budget_df["งบประมาณ_adjusted_for_plot"] = budget_df["งบประมาณ_adjusted"] * 4000 + 4500
budget_df[['lat', "lon"]] = location_df.loc[budget_df["ชื่อจังหวัด"], :].values
budget_df = budget_df.set_index("ชื่อจังหวัด")
reduced_budget_df = budget_df[budget_df.index != "บึงกาฬ"]

# 1. อัตราประชากรในจังหวัด (population df)
population_df = pd.read_csv("data/สถิติจำนวนประชากร_พื้นที่ ทั่วประเทศ.tsv", sep="\t")
population_df["รวม"] = population_df["รวม"].apply(remove_comma_and_convert_to_int)
population_df["พื้นที่"] = population_df["พื้นที่"].apply(remove_word_province)
population_df["รวม_adjusted"] = (population_df["รวม"].values - population_df["รวม"].values.mean()) / population_df["รวม"].values.std()
population_df = population_df.set_index("พื้นที่")

# 2. การเก็บภาษีจากแต่ละจังหวัด (tax df)
tax_df = pd.read_csv("data/y66_taxsumprov.csv")
tax_df["PROV"] = tax_df["PROV"].apply(lambda x: x.replace("กรุงเทพฯ", "กรุงเทพมหานคร"))
tax_df = tax_df.groupby("PROV")["AMT_RCV"].sum()
# tax_df = tax_df / population_df.loc[tax_df.index, "รวม"]
tax_df = (tax_df - tax_df.mean()) / tax_df.std()

# 3. บัตรสวัสดิการแห่งรัฐ หรือ ความยากจนของแต่จังหวัด (poverty df)
poverty_df = pd.read_csv("data/y66_province_poverty_with_province_name.csv")
poverty_df = poverty_df[["province_name", "JPT.MOFval.pov.rate"]].set_index("province_name")

# 4. รายได้ต่อหัวแต่ละจังหวัด (income_df)
income_df = pd.read_csv("data/y55-66 ค่าใช้จ่ายเฉลี่ยต่อเดือนของครัวเรือน เป็นรายภาค และจังหวัด.tsv", sep="\t")
income_df["2566"] = income_df["2566"].apply(remove_comma_and_convert_to_float)
income_df["2566_adjusted"] = (income_df["2566"].values - income_df["2566"].values.mean()) / income_df["2566"].values.std()
income_df = income_df[["จังหวัด", "2566_adjusted"]].set_index("จังหวัด")

x = []
province_used = []
for province in location_df.index:
    # กรุงเทพ and บึงกาฬ are missing in some dataset
    if province == "กรุงเทพมหานคร" or province == "บึงกาฬ": 
        continue
    province_used.append(province)
    x.append([
        budget_df.loc[province, "งบประมาณ_adjusted"],
        population_df.loc[province, "รวม_adjusted"],
        poverty_df.loc[province, "JPT.MOFval.pov.rate"],
        income_df.loc[province, "2566_adjusted"],
        tax_df.loc[province],
    ])

x = np.asarray(x)
mean = np.mean(x, axis=0)
cov = np.cov(x, rowvar=False)

p = np.asarray([mahalanobis_distance(xs, mean, cov) for xs in x])
p80 = np.quantile(p, 0.8)


hist_dist = alt.Chart(pd.DataFrame({"dist": p})).mark_bar().encode(
    alt.X("dist", bin=True), y="count()"
).properties(
    title="Histrogram of Mahalanobis Distance"
)

results_df = pd.DataFrame({
    "province": province_used,
    "dist": p,``
}).sort_values("dist", ascending=False).reset_index(drop=True)

map_plot_df = pd.DataFrame({
    "งบประมาณ_adjusted_for_plot": reduced_budget_df["งบประมาณ_adjusted_for_plot"],
    "lat": reduced_budget_df["lat"],
    "lon": reduced_budget_df["lon"],
    "color": [(34, 139, 34, 0.5) if pi < p80 else (211, 0, 0, 0.5) for pi in p],
})

# print("Sorted weirdness from most weird to not weird")
# reversd_idx = p.argsort()[::-1]
# print("rank\tProvince\tDist")
# for rank, idx in enumerate(reversd_idx):
#     print(f"{rank}\t{province_used[idx]}\t{p[idx].round(4)}")

# tsne_features = TSNE(n_components=2).fit_transform(x)
# plot_df = pd.DataFrame({
#     "tsne_x": tsne_features[:, 0],
#     "tsne_y": tsne_features[:, 1], 
#     "province": province_used,
#     # "color": ['g' if pi < p80 else 'r' for pi in p],
# })

# tsne_scatter = alt.Chart(plot_df).mark_point(
#     point={
#         "fill" : "green"
#     }
# ).encode(
#     x="tsne_x", y="tsne_y",
#     tooltip=["tsne_x", "tsne_y", "province"],
#     # color="color"
# )

st.title("Budget for All")
st.write("A :green[Green] dot indicates a normal province (< 80th percentiles mahalanobis distance). A :red[Red] dot indicates an abnormal province (>= 80th percentiles mahalanobis distance). The dot size indicate the amount of budget that each province will recieve.")
st.map(map_plot_df, size="งบประมาณ_adjusted_for_plot", color="color")
st.altair_chart(hist_dist, use_container_width=True)
st.write("Here's the table of mahalanobis distance on each province, sorted descending")
st.dataframe(results_df, use_container_width=True)
# st.altair_chart(tsne_scatter, use_container_width=True)
