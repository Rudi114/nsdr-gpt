# scrapes audio of input video + youtube's autogenerated subtitles
# urls come from the --batch-file
# and successful scraped urls are put into the --download-archive file
yt-dlp --extract-audio \
  --batch-file 10-minute-nsdr-urls.txt \
  --download-archive 10-min-nsdr-archive-write-auto-subs.txt \
  --output "./10_minute_nsdrs_write_auto_subs/%(title)s-%(id)s/%(title)s-%(id)s.%(ext)s" \
  --write-auto-subs \
  --sub-lang en