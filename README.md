# 🌍 글로벌 국가별 ETF 퍼포먼스

24개 국가 ETF의 기간별 수익률을 비교하는 차트입니다.

## 📈 포함 국가 (24개)

### Americas
| 티커 | 국가 |
|------|------|
| SPY | 미국 |
| EWC | 캐나다 |
| EWZ | 브라질 |
| EWW | 멕시코 |
| EPU | 페루 |
| ECH | 칠레 |

### Europe
| 티커 | 국가 |
|------|------|
| EWG | 독일 |
| EWQ | 프랑스 |
| EWU | 영국 |
| EWI | 이탈리아 |
| EWP | 스페인 |
| EWN | 네덜란드 |
| EWL | 스위스 |
| EPOL | 폴란드 |
| ENOR | 노르웨이 |
| TUR | 터키 |

### Asia / Pacific
| 티커 | 국가 |
|------|------|
| EWJ | 일본 |
| FXI | 중국 |
| INDA | 인도 |
| EWY | 한국 |
| EWT | 대만 |
| EWA | 호주 |
| VNM | 베트남 |

### Africa
| 티커 | 국가 |
|------|------|
| EZA | 남아공 |

## 🗓️ 기간 옵션

- 1주 (1W)
- 1개월 (1M)
- 3개월 (3M)
- 1년 (12M)
- 연초대비 (YTD) - 기본값

## 📡 데이터 소스

- **모든 자산**: Yahoo Finance (yfinance) - 무료

## ⚙️ 자동 업데이트

GitHub Actions가 매일 UTC 14:00 (한국시간 23:00)에 자동 실행됩니다.

## 🚀 배포

### GitHub Pages

1. Settings → Pages
2. Source: `main` branch
3. 자동 배포

### imweb

```html
<iframe 
  src="https://your-username.github.io/country-chart/" 
  width="100%" 
  height="750px" 
  style="border: none; border-radius: 12px;"
></iframe>
```

## 📁 구조

```
country-chart/
├── index.html
├── data/
│   └── performance.json
├── scripts/
│   ├── fetch_data.py
│   └── generate_html.py
└── .github/workflows/
    └── update-data.yml
```

## 📄 라이선스

MIT License
