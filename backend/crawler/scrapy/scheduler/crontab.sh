#!/bin/bash
source "/home/kth/dev/venv/bin/activate"
cd /home/kth/next/backend/crawler/scrapy/ondisk
scrapy crawl ondisk_update2 -a category=MVO >> goodlog.txt
