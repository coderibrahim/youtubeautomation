import pyttsx3
import os
import random
from moviepy.editor import *
from moviepy.video.fx import fadein, fadeout
import cv2
import time
from pymongo import MongoClient
import subprocess
import schedule
from upload_video import upload_video_to_yt
import ssl
import certifi
from moviepy.video.fx import fadein, fadeout


ca = certifi.where()
client = MongoClient("mongodb+srv://ibrahim:plaka65jk21706556..@cluster0.sboemja.mongodb.net/test", tlsCAFile=ca)

db = client["horror"]
collection = db["stories"]

def first_operations():
    random_story = collection.find_one({"isUsed": False})
    
    if random_story:
        story_id = random_story["_id"]
        story_main = random_story["storie"]
        story_title = random_story["title"]
        storyDescription = random_story["description"]
        storyKeywords = random_story["keywords"]

        collection.update_one({"_id": story_id}, {"$set": {"isUsed": True}})
        create_video(story_main, story_title, storyDescription, storyKeywords)
    else:
        print("All Stories are used.")


def create_video(story_main, story_title, storyDescription, storyKeywords):
    engine = pyttsx3.init()
    engine.setProperty('rate', 115)
    engine.setProperty('pitch', 60)

    text = story_main
    name = "Monroeville_Pennsylvania_horror_story"

    # Metni seslendirin ve ses dosyasını kaydedin
    engine.save_to_file(text, f"{name}_story.mp3")
    engine.runAndWait()  # Ses dosyasını tamamen oluşturduktan sonra devam edin

    # Rastgele bir şarkı seçin
    song_files = os.listdir("songs")
    song_file = os.path.join("songs", random.choice(song_files))

    # Şarkıyı ve hikaye sesini yükleyin
    audio_story = AudioFileClip(f"{name}_story.mp3")
    audio_song = AudioFileClip(song_file)

    # Metin seslendirme dosyasının süresini alın
    text_duration = audio_story.duration

    # Şarkının süresini alın
    song_duration = audio_song.duration

    # Şarkıyı metin seslendirme dosyasının süresine göre kırpın
    if song_duration > text_duration:
        audio_song = audio_song.subclip(0, text_duration)

    audio_song = audio_song.volumex(0.2)  # Ses seviyesini yarıya indirir
     
    final_audio = CompositeAudioClip([audio_story, audio_song])  # Şarkıyı ses dosyası ile birleştirin

    # Görüntüleri indirin ve boyutlandırarak birleştirin
    image_folder = "images"
    output_video = f"{name}.mp4"

    image_files = os.listdir(image_folder)
    random.shuffle(image_files)
    
    image_duration = text_duration / len(image_files)
    num_images = len(image_files)

    images = [ImageClip(os.path.join(image_folder, img)).set_duration(image_duration)
          for img in image_files[:num_images]]

    # Görüntüleri boyutlandırın ve çözünürlüğü ayarlayın
    width, height = 1920, 1080  # Hedef çözünürlük
    images_resized = []
    
    # Efekt eklemek için kullanılacak efektlerin listesi
    effects = [
        lambda x: x.fx(vfx.fadein, duration=2.0),  # Görüntüye 1 saniyelik bir fade-in efekti ekler
        lambda x: x.volumex(0.5),  # Ses seviyesini yarıya indirir
    ]

    for img_clip in images:
        img_array = img_clip.get_frame(0)
        img_resized = cv2.resize(img_array, (width, height))
        img_clip_resized = ImageClip(img_resized, duration=img_clip.duration)
        
        # Efektleri her görüntüye uygulayın
        for effect in effects:
            img_clip_resized = effect(img_clip_resized)

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
    intro_video = intro_video.set_duration(5)  # intro videosunun süresini sesin uzunluğuna ayarlayın

    # Son videoyu oluşturun ve sona rastgele bir video ekleyin video.set_audio(final_audio)
    final_video = concatenate_videoclips([intro_video, video.set_audio(final_audio)], method="compose")

    # Rastgele bir video alıp sonuna eklemek için
    endintro_folder = "endintro"
    endintro_files = os.listdir(endintro_folder)
    selected_endintro = os.path.join(endintro_folder, random.choice(endintro_files))
    endintro_clip = VideoFileClip(selected_endintro)
    final_video = concatenate_videoclips([final_video, endintro_clip.set_duration(5)], method="compose")


    # Yeniden düzenlenen videonuzu kaydedin
    final_video.write_videofile(output_video, codec=codec, bitrate=bitrate, audio_codec="aac")

    # Ses dosyasını ve ara dosyaları temizleyin
    os.remove(f"{name}_story.mp3")
    
    cleaned_title = story_title.strip("[]").strip()
    second_cleaned_title = cleaned_title.replace('"', '').replace('[', '').replace(']', '')

    cleaned_description = storyDescription.strip("[]").strip()
    second_cleaned_description = cleaned_description.replace('"', '').replace('[', '').replace(']', '')
    cleaned_keywords = storyKeywords.strip("[]").strip()
    temizlenmis_veri = [kelime.strip("' ") for kelime in cleaned_keywords.split(",")]
    sonuc = ", ".join(temizlenmis_veri)
    
    upload_video_to_yt(output_video, title=second_cleaned_title, description=second_cleaned_description, tags=sonuc)

first_operations()

schedule.every(4).hours.do(first_operations)

while True:
    schedule.run_pending()
    time.sleep(1)