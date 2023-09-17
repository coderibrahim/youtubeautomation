schedule.every().day.at("18:00").do(first_operations)

while True:
    schedule.run_pending()
    time.sleep(1)
    
     upload_video_command = [
        "python",  # Python yürütücüsünü çağır
        "upload_video.py",  # Yürütmek istediğiniz betik dosyasının adı
        f"--file={output_video}",  # Video dosyasının yolunu ver
        f"--title={story_title}",  # Video başlığı
        f"--description={cleaned_description}",  # Video açıklaması
        f"--keywords={storyKeywords}",  # Anahtar kelimeler
        "--category=39",  # Kategori
        "--privacyStatus=public"  # Gizlilik durumu
    ]

    # upload_video.py dosyasını çağır
    try:
        subprocess.run(upload_video_command, check=True)
        print("Video yüklemesi başarıyla tamamlandı.")
    except subprocess.CalledProcessError as e:
        print(f"Video yükleme hatası: {e}")
        