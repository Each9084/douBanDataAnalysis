import requests
from bs4 import BeautifulSoup
import time
import random
import re
import pandas as pd

BASE_URL = "https://movie.douban.com/top250"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}


def parse_movie_item(item):
    """解析单个电影条目"""
    title_spans = item.select("div.hd span.title")
    titles = [s.get_text(strip=True) for s in title_spans]
    title = " / ".join(titles)

    other = item.select_one("div.hd span.other")
    original_title = other.get_text(strip=True) if other else ""

    info_p = item.select_one("div.bd p")
    info_text = ""
    if info_p:
        info_text = info_p.get_text(separator=" ").strip()
        info_text = re.sub(r"\s+", " ", info_text)

    year_match = re.search(r"(\d{4})", info_text)
    year = year_match.group(1) if year_match else ""

    tail = ""
    try:
        parts = [p.strip() for p in info_text.split('/') if p.strip()]
        idx = next((i for i, p in enumerate(parts) if re.search(r"\d{4}", p)), None)
        if idx is not None:
            tail = " / ".join(parts[idx + 1:])
    except Exception:
        tail = ""

    try:
        rating = item.select_one("span.rating_num").get_text(strip=True)
    except AttributeError:
        rating = ""

    try:
        spans = item.select("div.bd div > span")
        num_ratings = ""
        for sp in spans:
            text = sp.get_text(strip=True)
            if "人评价" in text:
                num_ratings = re.search(r"([\d,]+)", text).group(1).replace(",", "")
                break
    except Exception:
        num_ratings = ""

    try:
        quote = item.select_one("p.quote span").get_text(strip=True)
    except AttributeError:
        quote = ""

    return {
        "title": title,
        "original_title": original_title,
        "info_text": info_text,
        "year": year,
        "tail": tail,
        "rating": rating,
        "num_ratings": num_ratings,
        "quote": quote
    }


def fetch_top250(save_csv="data/raw/douban_top250_raw.csv"):
    """抓取豆瓣 Top250 并保存 CSV"""
    all_movies = []
    for start in range(0, 250, 25):
        params = {"start": start}
        print(f"Fetching start={start} ...")
        try:
            resp = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"Request failed for start={start}: {e}")
            time.sleep(5)
            continue

        soup = BeautifulSoup(resp.text, "lxml")
        items = soup.select("div.item")
        if not items:
            print("No items found on page — maybe blocked or page structure changed.")
            break

        for it in items:
            data = parse_movie_item(it)
            all_movies.append(data)

        time.sleep(random.uniform(1.0, 2.5))

    df = pd.DataFrame(all_movies)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["num_ratings"] = pd.to_numeric(df["num_ratings"], errors="coerce")

    df.to_csv(save_csv, index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} records to {save_csv}")
    return df
