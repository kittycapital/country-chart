#!/usr/bin/env python3
"""
글로벌 국가별 ETF 성과 데이터 수집 스크립트
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'yfinance', '-q'])
    import yfinance as yf

# ============================================
# 글로벌 국가 ETF 정의 (24개국)
# ============================================

ASSETS = {
    # Americas
    "SPY": {"name": "미국", "color": "#3b82f6"},
    "EWC": {"name": "캐나다", "color": "#ef4444"},
    "EWZ": {"name": "브라질", "color": "#22c55e"},
    "EWW": {"name": "멕시코", "color": "#f59e0b"},
    "EPU": {"name": "페루", "color": "#8b5cf6"},
    "ECH": {"name": "칠레", "color": "#06b6d4"},
    
    # Europe
    "EWG": {"name": "독일", "color": "#ec4899"},
    "EWQ": {"name": "프랑스", "color": "#84cc16"},
    "EWU": {"name": "영국", "color": "#f97316"},
    "EWI": {"name": "이탈리아", "color": "#14b8a6"},
    "EWP": {"name": "스페인", "color": "#a855f7"},
    "EWN": {"name": "네덜란드", "color": "#eab308"},
    "EWL": {"name": "스위스", "color": "#64748b"},
    "EPOL": {"name": "폴란드", "color": "#dc2626"},
    "ENOR": {"name": "노르웨이", "color": "#0891b2"},
    "TUR": {"name": "터키", "color": "#c026d3"},
    
    # Asia / Pacific
    "EWJ": {"name": "일본", "color": "#e11d48"},
    "FXI": {"name": "중국", "color": "#ea580c"},
    "INDA": {"name": "인도", "color": "#16a34a"},
    "EWY": {"name": "한국", "color": "#2563eb"},
    "EWT": {"name": "대만", "color": "#7c3aed"},
    "EWA": {"name": "호주", "color": "#0d9488"},
    "VNM": {"name": "베트남", "color": "#ca8a04"},
    
    # Africa
    "EZA": {"name": "남아공", "color": "#be185d"},
}


def get_date_ranges():
    """기간별 시작 날짜 계산"""
    today = datetime.now()
    
    return {
        "1W": today - timedelta(days=7),
        "1M": today - timedelta(days=30),
        "3M": today - timedelta(days=90),
        "12M": today - timedelta(days=365),
        "YTD": datetime(today.year, 1, 1),
    }


def fetch_etf_data(symbol, days=400):
    """yfinance로 ETF 데이터 가져오기"""
    print(f"  📈 {symbol} 데이터 수집 중...")
    
    try:
        ticker = yf.Ticker(symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        hist = ticker.history(start=start_date, end=end_date)
        
        if hist.empty:
            print(f"  ⚠️ {symbol} 데이터 없음")
            return None
        
        # 날짜와 종가만 추출
        data = []
        for date, row in hist.iterrows():
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "price": round(row["Close"], 2)
            })
        
        print(f"  ✅ {symbol}: {len(data)}일 데이터")
        return data
        
    except Exception as e:
        print(f"  ❌ {symbol} 오류: {e}")
        return None


def calculate_performance(prices, start_date):
    """특정 날짜부터의 수익률 계산"""
    start_str = start_date.strftime("%Y-%m-%d")
    
    # 시작 날짜에 가장 가까운 데이터 찾기
    start_price = None
    for p in prices:
        if p["date"] >= start_str:
            start_price = p["price"]
            break
    
    if not start_price or not prices:
        return None
    
    end_price = prices[-1]["price"]
    return round((end_price - start_price) / start_price * 100, 2)


def main():
    print("=" * 50)
    print("🚀 글로벌 국가 ETF 데이터 수집 시작")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    date_ranges = get_date_ranges()
    all_data = {}
    
    # 모든 ETF 데이터 수집
    print("\n📊 국가 ETF 데이터 수집")
    for symbol, info in ASSETS.items():
        prices = fetch_etf_data(symbol)
        if prices:
            all_data[symbol] = {
                "name": info["name"],
                "color": info["color"],
                "prices": prices,
                "performance": {}
            }
            
            # 기간별 수익률 계산
            for period, start_date in date_ranges.items():
                perf = calculate_performance(prices, start_date)
                all_data[symbol]["performance"][period] = perf
    
    # 결과 저장
    output = {
        "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "assets": all_data
    }
    
    output_path = Path(__file__).parent.parent / "data" / "performance.json"
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print(f"✅ 완료! {len(all_data)}개 국가 저장됨")
    print(f"📁 {output_path}")
    print("=" * 50)
    
    # YTD 성과 출력
    print("\n📊 YTD 성과:")
    for symbol, data in sorted(all_data.items(), key=lambda x: x[1]["performance"].get("YTD", 0) or 0, reverse=True):
        perf = data["performance"].get("YTD", "N/A")
        if perf is not None:
            sign = "+" if perf >= 0 else ""
            print(f"  {symbol:5} {data['name']:10} {sign}{perf}%")


if __name__ == "__main__":
    main()
