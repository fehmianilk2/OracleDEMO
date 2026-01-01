import yfinance as yf

print("🔍 Apple hissesi için bağlantı test ediliyor...")

try:
    # Sadece Apple'ı çekmeyi dene ve hatayı gizleme
    apple = yf.Ticker("AAPL")
    hist = apple.history(period="5d")
    
    if hist.empty:
        print("❌ HATA: Veri boş geldi! (Yahoo erişimi engelliyor olabilir)")
    else:
        print("✅ BAŞARILI! Veri alındı:")
        print(hist.tail())

except Exception as e:
    print(f"❌ KRİTİK HATA: {e}")