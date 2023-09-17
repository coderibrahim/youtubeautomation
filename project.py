import pyttsx3
import os
import random
from moviepy.editor import *
import cv2


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

# Görüntüleri indirin ve boyutlandırarak birleştirin
image_folder = "images"
output_video = f"{name}.mp4"

image_files = os.listdir(image_folder)
random.shuffle(image_files)

images = [ImageClip(os.path.join(image_folder, img)).set_duration(5)
          for img in image_files[:3]]  # İlk 3 görüntüyü kullanabilirsiniz

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

# Intro videosunu seçin
intro_folder = "intro"
intro_files = os.listdir(intro_folder)
selected_intro = os.path.join(intro_folder, random.choice(intro_files))

# Intro videosunu projenin başına ekleyin
intro_video = VideoFileClip(selected_intro)
intro_video = intro_video.set_duration(audio_duration)  # intro videosunun süresini sesin uzunluğuna ayarlayın

# Son videoyu oluşturun ve sona rastgele bir video ekleyin
final_video = concatenate_videoclips([intro_video.crossfadein(5), video.set_audio(final_audio)], method="compose")

# Rastgele bir video alıp sonuna eklemek için
endintro_folder = "endintro"
endintro_files = os.listdir(endintro_folder)
selected_endintro = os.path.join(endintro_folder, random.choice(endintro_files))
endintro_clip = VideoFileClip(selected_endintro)
final_video = concatenate_videoclips([final_video, endintro_clip], method="compose")

# Yeniden düzenlenen videonuzu kaydedin
final_video.write_videofile(output_video, codec=codec, bitrate=bitrate, audio_codec="aac")

# Ses dosyasını ve ara dosyaları temizleyin
os.remove(f"{name}.mp3")

print("Video oluşturuldu:", output_video)
