
# Günlük işi planla (her gün saat 18:00'de çalışacak)
schedule.every().day.at("18:00").do(first_operations)

while True:
    schedule.run_pending()
    time.sleep(1)