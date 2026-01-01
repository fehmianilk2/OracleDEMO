"""
🦅 AESTHESIUS MARKET ORACLE (DEMO VERSION - FINAL)
--------------------------------------------------
Developer: Anıl (Aesthesius)
Version: 1.4 (Demo Limit Added)
"""

import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import sys

# --- AYARLAR ---
WATCHLIST = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META", "AMD", "COIN"]
RSI_PERIOD = 14
OVERSOLD_LEVEL = 30
OVERBOUGHT_LEVEL = 70
DEMO_LIMIT = 5  # Bot kaç tur çalışıp kapansın? (5 tur idealdir)

def print_header():
    print("\033[92m") # Parlak Yeşil
    print(r"""
     _    ____ ____ _____ _   _ _____ ____ ___ _   _ ____  
    / \  |  __|  __|__ __| | | |  __|  __||_ _| | | |  __| 
   / _ \ |  __|__  |  |  | |_| |  __|__  | | || |_| |__  | 
  /_/ \_\|____|____|  |  |_|___|____|____|___|___/|____| 
     >>> MARKET ORACLE SYSTEM v1.4 (DEMO) <<<
    """)
    print("\033[0m") 

def calculate_rsi(ticker):
    try:
        stock = yf.Ticker(ticker)
        # Period 1y: Garanti veri
        df = stock.history(period="1y", interval="1d")

        if df.empty or len(df) < RSI_PERIOD:
            return None, 0

        # RSI HESAPLAMA
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=RSI_PERIOD).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=RSI_PERIOD).mean()

        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        if pd.isna(df['RSI'].iloc[-1]):
             last_rsi = df['RSI'].iloc[-2]
        else:
             last_rsi = df['RSI'].iloc[-1]
             
        last_price = df['Close'].iloc[-1]

        return last_rsi, last_price

    except Exception as e:
        return None, 0

def analyze_market():
    print("-" * 75)
    print(f"🕒 TARAMA ZAMANI: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 75)
    print(f"{'SEMBOOL':<10} {'FİYAT ($)':<12} {'RSI':<10} {'DURUM / SİNYAL'}")
    print("-" * 75)

    for symbol in WATCHLIST:
        rsi, price = calculate_rsi(symbol)

        if rsi is None:
            continue

        signal = "Nötr"
        icon = "⚪"
        
        if rsi <= OVERSOLD_LEVEL:
            signal = "AŞIRI SATIM (AL?)"
            icon = "🟢 STRONG BUY"
        elif rsi >= OVERBOUGHT_LEVEL:
            signal = "AŞIRI ALIM (SAT?)"
            icon = "🔴 STRONG SELL"
        elif 30 < rsi < 45:
            signal = "Düşük Bölge"
            icon = "📉"
        elif 55 < rsi < 70:
            signal = "Yüksek Bölge"
            icon = "📈"

        print(f"{symbol:<10} {price:<12.2f} {rsi:<10.1f} {icon} {signal}")
        time.sleep(0.2) 

    print("-" * 75)
    print("\n")

if __name__ == "__main__":
    try:
        print_header()
        print(f"Sistem başlatılıyor... (Demo Modu: {DEMO_LIMIT} Tarama ile sınırlıdır)")
        time.sleep(2)
        
        loop_count = 0
        
        while loop_count < DEMO_LIMIT:
            loop_count += 1
            print(f"🔄 Döngü: {loop_count}/{DEMO_LIMIT}")
            
            analyze_market()
            
            # Son turdaysa beklemeye gerek yok, direkt bitir
            if loop_count == DEMO_LIMIT:
                break
                
            for i in range(10, 0, -1): # Demo olduğu için bekleme süresini 10 sn yaptım, hızlı aksın
                sys.stdout.write(f"\r⏳ Sıradaki tarama: {i} sn...   ")
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write("\r" + " " * 40 + "\r")

        # --- KAPANIŞ MESAJI ---
        print("\n" + "="*50)
        print("✅ DEMO SÜRECİ BAŞARIYLA TAMAMLANDI.")
        print("💡 Bu sadece bir önizlemedir (Preview).")
        print("🦅 Tam Sürüm ve Telegram Entegrasyonu için:")
        print("   >> Developer: Anıl (Aesthesius)")
        print("="*50 + "\n")

    except KeyboardInterrupt:
        print("\n\n🦅 Aesthesius Oracle kullanıcı tarafından kapatıldı.")