import pyttsx3
import os
import random
import cv2
from moviepy.editor import *

# Metni seslendiren TTS motorunu oluşturun
engine = pyttsx3.init()
engine.setProperty('rate', 140)
engine.setProperty('pitch', 10)

text = "I live up in Monroeville, Pennsylvania. For those who don’t know, it’s a historical site when it comes to horror movies; being that it has the mall where they recorded the original Dawn of the Dead back in 1977."
name = "Monroeville_Pennsylvania_horror_story"

# Metni seslendirin ve ses dosyasını kaydedin
engine.save_to_file(text, f"{name}.mp3")
engine.runAndWait()  # Ses dosyasını tamamen oluşturduktan sonra devam edin

# Rastgele bir şarkı seçin ve ses dosyası ile birleştirin
song_files = os.listdir("songs")
audio = AudioFileClip(f"{name}.mp3")
song = AudioFileClip(os.path.join("songs", random.choice(song_files)))
audio_duration = audio.duration  # Ses süresini alın
final_audio = CompositeAudioClip([audio, song.set_duration(audio_duration)])  # Şarkıyı ses dosyası ile birleştirin

# Intro videosunu seçin
intro_folder = "intro"
intro_files = os.listdir(intro_folder)
selected_intro = os.path.join(intro_folder, random.choice(intro_files))

# Intro videosunu projenin başına ekleyin
intro_video = VideoFileClip(selected_intro)
intro_video = intro_video.set_duration(audio_duration)  # intro videosunun süresini sesin uzunluğuna ayarlayın

# Görüntüleri indirin ve boyutlandırarak birleştirin
image_folder = "images"
output_video = f"{name}.mp4"

image_files = os.listdir(image_folder)
random.shuffle(image_files)

# Geçiş efektlerini belirleyin
gecis_suresi = 1.5  # Geçiş süresi (saniye)

images = []
for i, img_file in enumerate(image_files):
    img_path = os.path.join(image_folder, img_file)
    img_clip = ImageClip(img_path).set_duration(5)
    
    # İlk fotoğraf için geçiş efekti uygulama
    if i == 0:
        images.append(img_clip)
    else:
        prev_img_clip = images[i - 1]
        img_clip = img_clip.set_start(prev_img_clip.end - gecis_suresi)  # Geçiş süresini ayarla
        img_clip = img_clip.crossfadein(gecis_suresi)  # Geçiş efekti uygula
        images.append(img_clip)

# Görüntüleri boyutlandırın ve çözünürlüğü ayarlayın
width, height = 1280, 720  # Hedef çözünürlük
images_resized = []
for img_clip in images:
    img_array = img_clip.get_frame(0)
    img_resized = cv2.resize(img_array, (width, height))
    img_clip_resized = ImageClip(img_resized, duration=img_clip.duration)
    images_resized.append(img_clip_resized)

video = concatenate_videoclips(images_resized, method="compose")

# Video çözünürlüğünü, FPS'i, codec'i ve video bitrate'ini ayarlayın
video = video.resize(width=width, height=height)
video.fps = 30  # FPS değerini ayarlayın
codec = "libx264"  # Video codec'i
bitrate = "2000k"  # Video bitrate'i (örnek değer)

# Ses dosyasını videoya ekleyin ve final_video'yu tanımlayın
final_video = concatenate_videoclips([intro_video, video.set_audio(final_audio)], method="compose")

# Yeniden düzenlenen videonuzu kaydedin
final_video.write_videofile(output_video, codec=codec, bitrate=bitrate, audio_codec="aac")

# Ses dosyasını ve ara dosyaları temizleyin
os.remove(f"{name}.mp3")

print("Video oluşturuldu:", output_video)
