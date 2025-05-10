<h1>Auto Video Creator & Publisher for YouTube</h1>
<hr>
<p>
This project is a fully automated system designed to create and publish videos on YouTube with minimal manual input. It follows a smart pipeline to generate engaging content using data from a MongoDB database and media assets stored locally.
</p>

<h2>Key Features</h2>
<ul>
  <li><strong>Automated Content Retrieval:</strong> Video titles and scripts are fetched directly from a MongoDB database.</li>
  <li><strong>Media Integration:</strong> Background images are selected and aligned with the video duration. Background music and voiceover are automatically added based on the script.</li>
  <li><strong>AI Voice Narration:</strong> The content is converted into speech using text-to-speech technologies.</li>
  <li><strong>Video Composition:</strong> Images, voiceovers, and background music are compiled into a final video.</li>
  <li><strong>YouTube Publishing:</strong> The generated video is automatically uploaded to a linked YouTube account.</li>
  <li><strong>Optional GPT Integration:</strong> For dynamic content generation, ChatGPT can be integrated to create titles, descriptions, or entire scripts.</li>
</ul>

<h2>Technology Stack</h2>
<ul>
  <li>MongoDB for content storage</li>
  <li>FFmpeg or similar tools for video rendering</li>
  <li>Text-to-Speech API (e.g., Google TTS, AWS Polly)</li>
  <li>YouTube Data API for video upload</li>
  <li>Optional: OpenAI GPT for AI-generated content</li>
</ul>
