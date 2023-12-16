#00 0,12 * * * /home/kth/next/backend/crawler/scrapy/ondisk/ondisk_movie.sh > /var/log/crontab.kog 2>%1
#00 3,15 * * * /home/kth/next/backend/crawler/scrapy/ondisk/ondisk_drama.sh > /var/log/crontab.kog 2>%1
#00 6,18 * * * /home/kth/next/backend/crawler/scrapy/ondisk/ondisk_media.sh > /var/log/crontab.kog 2>%1
#00 9,21 * * * /home/kth/next/backend/crawler/scrapy/ondisk/ondisk_ani.sh > /var/log/crontab.kog 2>%1
#* * * * * /home/kth/next/backend/crawler/scrapy/ondisk/ondisk_movie.sh > /var/log/crontab.kog 2>%1
00 0,12 * * * timeout 14400 cd ~; ./crontab.sh
00 3,15 * * * timeout 14400 cd ~/next/backend/crawler/scrapy/scheduler;./ondisk2.sh

