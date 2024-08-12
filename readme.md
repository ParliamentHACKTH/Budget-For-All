# Budget for All: Web app for showing Mahalanobis Distance

This is a web app for visualizing Mahalanobis Distance on each province, written in streamlit. The core idea of this app is to apply some unsupervised learning technique to the anomaly detection task. Then, display the result in the map for the human checker. The page 8 and 9 in the [slide](https://hack.parliament.go.th/storage/slide/31.pdf) here describe the dataset and the algorithm of this repo.

![web home page](readme_assets/web%20home%20page.png)

## Datasets

The dataset we used is consist of 5 sources.
1. The proposed budget of each province for year 2025 (`y68 Thailand's Budget per จังหวัด.tsv`)
2. The tax collected of each province for year 2023 (`y66_taxsumprov.csv`)
3. The proverty rate of each province for year 2023 (`y66_province_poverty_with_province_name.csv`)
4. The population of each province for year 2023 (`สถิติจำนวนประชากร_พื้นที่ ทั่วประเทศ.tsv`)
5. The average cost per family of each province for year 2023 (`y55-66 ค่าใช้จ่ายเฉลี่ยต่อเดือนของครัวเรือน เป็นรายภาค และจังหวัด.tsv`)

## Algorithms

The algorithm we used, Mahalanobis Distance, is an unsupervised learning technique that has been used for anomaly detection task as it is pretty easy to interpret. The result number is just kinda distance from mean, as the number increase, the weirder (far from mean) it gets.

However, the algorithm requires the data to be independence from each other, in which the datasets above doesn't be. And in my personal believe, 5 datasets are probably not enough.

## Run The Web App

### Install dependencies

1. Install Python 3.9.5
2. Install the rest of dependencies via
    ```bash
    pip install -r requirements.txt
    ```

### Run

```bash
streamlit run app.py
```

## Authors

This repository is a part of work from the Hackathon [Open Parliament Hack 2024](https://hack.parliament.go.th/) from the team Budget For All. All of the code are written by [ACitronella](https://github.com/ACitronella).
