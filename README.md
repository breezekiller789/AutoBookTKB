# Installation

- Install Google Chrome
- `pip install selenium`
- Download and unzip `chromedriver` from https://chromedriver.storage.googleapis.com/index.html?path=85.0.4183.38/
- Put `chromedriver` in `$PATH`
- Write settings to `AutoBookTKB/AutoBookTKB-settings.json`. Example:

```json
{
    "id": "SXXXXXXX",
    "password": "XXXX",
    "classIndex": "1",
    "location": "高雄數位學堂",
    "sessions": [
        3
    ]
}
```

- Run it: `python AutoBookTKB/AutoBookTKB.py`

# Original README

**AutoBookTKB** 是一個簡單輕巧的軟體，幫助學生自動預約TKB數位學堂的上課座位。
  
--------------------------
**WIN10 64位元**的使用者可直接使用本專案[dist.rar](https://github.com/heyfey/AutoBookTKB/blob/master/dist.rar)中包含的可執行檔。(或[在此](https://drive.google.com/open?id=1Z2_myn0V9EGksSFVX_NGtw2HxfhmU593)下載)
  
其他作業系統(**Mac / Ubuntu / Linux**)的使用者：
1. 請直接下載完整的專案。
2. 將`AutoBookTKB`資料夾中的網頁驅動(`chromedriver.exe`)，替換成與作業系統對應的驅動軟體(在`chromedriver`資料夾中)
3. 用[python](https://www.python.org/downloads/)執行 **_AutoBookTKB-GUI.py_**  (`python AutoBookTKB-GUI.py`)
4. Required package：[Selenium ](https://selenium-python.readthedocs.io/installation.html)
  
--------------------------
**Preview：**
  
![](https://i.imgur.com/zt4GWnU.png)
  
>**預約日期將是下次釋出可預約座位的最新日期，即一個禮拜後。**
  
  
--------------------------
如果有任何問題：
tsungtsohsieh@gmail.com
