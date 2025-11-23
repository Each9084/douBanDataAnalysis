from src.scraper.douban_scraper import fetch_top250

if __name__ == "__main__":
    df = fetch_top250()
    print(df.head())
