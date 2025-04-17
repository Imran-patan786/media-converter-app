import gradio as gr
import os
from PIL import Image
import ffmpeg
from pydub import AudioSegment
import PyPDF2
from docx import Document
import numpy as np
from pytube import YouTube
import instaloader

# Image Format Converter
def image_converter(input_img, format):
    img = Image.open(input_img)
    output_path = f"converted_image.{format.lower()}"
    img.save(output_path, format.upper())
    return output_path

# Video to Audio Converter
def video_to_audio(video_file):
    try:
        stream = ffmpeg.input(video_file)
        output_path = "extracted_audio.mp3"
        stream = ffmpeg.output(stream, output_path, format='mp3', acodec='mp3', vn=True)
        ffmpeg.run(stream)
        return output_path
    except Exception as e:
        return f"Error: {str(e)}"

# Audio Format Converter
def audio_converter(audio_file, format):
    audio = AudioSegment.from_file(audio_file)
    output_path = f"converted_audio.{format}"
    audio.export(output_path, format=format)
    return output_path

# Video Format Converter
def video_converter(video_file, format):
    try:
        stream = ffmpeg.input(video_file)
        output_path = f"converted_video.{format}"
        stream = ffmpeg.output(stream, output_path)
        ffmpeg.run(stream)
        return output_path
    except Exception as e:
        return f"Error: {str(e)}"

# Image Enhancer
def enhance_image(input_img, brightness, contrast):
    img = Image.open(input_img)
    img_array = np.array(img)
    enhanced = np.clip(img_array * brightness * contrast, 0, 255).astype(np.uint8)
    output_img = Image.fromarray(enhanced)
    output_path = "enhanced_image.jpg"
    output_img.save(output_path)
    return output_path

# Document Format Converter
def doc_converter(input_file, format):
    output_path = f"converted_doc.{format}"
    if input_file.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(input_file)
        if format == 'docx':
            doc = Document()
            for page in pdf_reader.pages:
                doc.add_paragraph(page.extract_text())
            doc.save(output_path)
    elif input_file.endswith('.docx'):
        if format == 'pdf':
            return "DOCX to PDF not implemented in this basic version"
    return output_path

# YouTube Downloader
def youtube_downloader(link, media_type):
    try:
        yt = YouTube(link)
        if media_type == 'audio':
            audio_stream = yt.streams.filter(only_audio=True).first()
            output_path = "youtube_audio.mp4"
            audio_stream.download(output_path=output_path)
            return output_path
        elif media_type == 'video':
            video_stream = yt.streams.get_highest_resolution()
            output_path = "youtube_video.mp4"
            video_stream.download(output_path=output_path)
            return output_path
    except Exception as e:
        return f"Error: {str(e)}"

# Instagram Downloader
def instagram_downloader(link, media_type):
    try:
        L = instaloader.Instaloader()
        post = instaloader.Post.from_url(L.context, link)
        if media_type == 'audio':
            return "Audio download from Instagram is not supported"
        elif media_type == 'video':
            video_url = post.video_url
            output_path = "instagram_video.mp4"
            L.download_url(video_url, output_path=output_path)
            return output_path
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio Interface
with gr.Blocks(title="RSP'S Media Converter") as demo:
    gr.Markdown("# Media Converter Suite")

    with gr.Tab("Image Format Converter"):
        with gr.Row():
            img_input = gr.Image(type="filepath", label="Upload Image")
            img_format = gr.Dropdown(["PNG", "JPG", "WEBP"], label="Output Format")
        img_output = gr.File(label="Converted Image")
        gr.Button("Convert").click(image_converter, inputs=[img_input, img_format], outputs=img_output)

    with gr.Tab("Video to Audio"):
        vid_input = gr.Video(label="Upload Video")
        aud_output = gr.Audio(label="Extracted Audio")
        gr.Button("Extract Audio").click(video_to_audio, inputs=vid_input, outputs=aud_output)

    with gr.Tab("Audio Format Converter"):
        with gr.Row():
            aud_input = gr.Audio(type="filepath", label="Upload Audio")
            aud_format = gr.Dropdown(["mp3", "wav", "ogg"], label="Output Format")
        aud_conv_output = gr.File(label="Converted Audio")
        gr.Button("Convert").click(audio_converter, inputs=[aud_input, aud_format], outputs=aud_conv_output)

    with gr.Tab("Video Format Converter"):
        with gr.Row():
            vid_conv_input = gr.Video(label="Upload Video")
            vid_format = gr.Dropdown(["mp4", "avi", "mov"], label="Output Format")
        vid_conv_output = gr.File(label="Converted Video")
        gr.Button("Convert").click(video_converter, inputs=[vid_conv_input, vid_format], outputs=vid_conv_output)

    with gr.Tab("Image Enhancer"):
        with gr.Row():
            enhance_input = gr.Image(type="filepath", label="Upload Image")
            brightness = gr.Slider(0.5, 2, value=1, label="Brightness")
            contrast = gr.Slider(0.5, 2, value=1, label="Contrast")
        enhance_output = gr.Image(label="Enhanced Image")
        gr.Button("Enhance").click(enhance_image, inputs=[enhance_input, brightness, contrast], outputs=enhance_output)

    with gr.Tab("Document Converter"):
        with gr.Row():
            doc_input = gr.File(label="Upload Document")
            doc_format = gr.Dropdown(["pdf", "docx"], label="Output Format")
        doc_output = gr.File(label="Converted Document")
        gr.Button("Convert").click(doc_converter, inputs=[doc_input, doc_format], outputs=doc_output)

    with gr.Tab("YouTube Downloader"):
        with gr.Row():
            yt_link = gr.Textbox(label="Enter YouTube Link")
            yt_media_type = gr.Dropdown(["audio", "video"], label="Select Media Type")
        yt_output = gr.File(label="Downloaded Media")
        gr.Button("Download").click(youtube_downloader, inputs=[yt_link, yt_media_type], outputs=yt_output)

    with gr.Tab("Instagram Downloader"):
        with gr.Row():
            insta_link = gr.Textbox(label="Enter Instagram Link")
            insta_media_type = gr.Dropdown(["audio", "video"], label="Select Media Type")
        insta_output = gr.File(label="Downloaded Media")
        gr.Button("Download").click(instagram_downloader, inputs=[insta_link, insta_media_type], outputs=insta_output)

demo.launch(server_name="0.0.0.0", server_port=10000)
