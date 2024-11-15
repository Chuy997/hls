@echo off
ffmpeg -i rtsp://admin:Test.2024@10.232.118.195:554/LiveMedia/ch1/Media1 -r 20 -vf scale=1280:720 -b:v 1000k -preset veryfast -g 60 -c:v libx264 -c:a aac -f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments+append_list C:/xampp/htdocs/hls/static/hls/index.m3u8
pause
