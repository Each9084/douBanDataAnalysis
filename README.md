# DouBan Data Analysis

## 项目简介
这是一个 Python 数据分析项目，用于爬取豆瓣电影 Top250 数据，并进行数据清洗、分析和可视化。项目结构模块化，便于多人协作和未来扩展（如词云、统计分析等）。

主要功能：
- 爬取豆瓣 Top250 电影信息（标题、原名、年份、导演、主演、评分、评价人数、经典台词）
- 数据清洗并保存为 CSV
- 数据分析和可视化（matplotlib、词云等）
- 多人协作规范化项目结构

---

## 项目结构

douBanDataAnalysis/
 ├─ .gitignore(自动忽略.venv)
 ├─ README.md
 ├─ requirements.txt
 ├─ data/
 │   ├─ raw/               # 爬取的原始 CSV
 │   └─ processed/         # 清洗后的数据
 ├─ src/
 │   ├─ scraper/           # 爬虫模块
 │   │   ├─ **init**.py
 │   │   └─ douban_scraper.py
 │   ├─ clean/             # 数据清洗模块
 │   │   ├─ **init**.py
 │   │   └─ clean_data.py
 │   ├─ analysis/          # 数据分析模块
 │   │   ├─ **init**.py
 │   │   └─ analyze.py
 │   └─visualization/     # 可视化模块
 │   
 └─ tests/                 # 单元测试
 ├─ **init**.py
 └─ main.py

---

## 安装与依赖

1. 克隆仓库
```bash
git clone https://github.com/Each9084/douBanDataAnalysis.git
cd douBanDataAnalysis
```

1. 创建虚拟环境

```
python -m venv venv
```

1. 激活虚拟环境

- Windows:

```
venv\Scripts\activate
```

- macOS/Linux:

```
source venv/bin/activate
```

1. 安装依赖

```
pip install -r requirements.txt
```
