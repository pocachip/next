this is my next project (by pocachip 2023-10-17)
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

#crontab
1. select-editor (default crontab editer -->2)
2. crontab -e
   * * * * * doitnow.sh (1분마다 실행)
   */10 * * * * doitnow.sh (10분마다 실행)
   15 * * * * doitnow.sh (매시 15분마다 실행)
   0 * * * * doitnow.sh (매시간 실행)
   0 */2 * * * doitnow.sh (2시간마다 실행)
   00 11,16 * * * /home/ramesh/bin/incremental-backup (11시 16시 실행)
   00 09-18 * * * /home/ramesh/bin/check-db-status (9~18시 매시간 실행)
   00 09-18 * * 1-5 /home/ramesh/bin/check-db-status (주말 제외 Sunday=0)
   30 23 * * *   timeout 18000  /usr/bin/php /var/www/ul/prices_all.php >> /var/www/ul/log/prices_all.txt (5시간 이후 자동 멈춤)
 
3. service cron staus
  service cron start(restart/stop) 
4. kill 특정 크론 명령
pkill -f 'wget -q -O - https://happist.com/wp-cron.php?doing_wp_cron >/dev/null 2>&1'

#mysql columns 변경
select count(idx), DATE_FORMAT(STR_TO_DATE(REPLACE(last_update, '"', ''), '%Y-%m-%d %H:%i:%s'), '%Y-%m-%d %H') from rightwatch.post
group by DATE_FORMAT(STR_TO_DATE(REPLACE(last_update, '"', ''), '%Y-%m-%d %H:%i:%s'), '%Y-%m-%d %H');

select count(idx), DATE_FORMAT(last_update, '%Y-%m-%d %H') from rightwatch.post
group by DATE_FORMAT(last_update, '%Y-%m-%d %H');

alter table rightwatch.post add column last_update2 DATETIME;
alter table rightwatch.post drop last_update;
alter table rightwatch.post drop last_update1;
alter table rightwatch.post change last_update2 last_update DATETIME;
update rightwatch.post
set last_update2 = str_to_date(REPLACE(last_update, '"', ''), '%Y-%m-%d %H:%i:%s');

#ngx-admin은 
nvm ls-remote
1.install node 14.21.3
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
  source ~/.bashrc
  nvm --version
  nvm list
  
2. rmp run got some error('Server bla bla...')
3. npm i --save @types/ws@8.5.4

#code style
1. Camel case
	camel case => camelCase
2. Kebab case
	kebab case => kebab-case
3. Snake case
	snake case => SNAKE_CASE
4. Pascal case
	pascal case => PascalCase

#ngx-admin starter-kit install 시 python2를 찾아서 깔어줌
python2 설치 
	sudo add-apt-repository universe
	sudo apt update 
	sudo apt install python2
	curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
	sudo python2 get-pip.py
	pip2 --version

#pakage.json dependance 업데이트를 위해 --save-dev 를 해야한다.
npm install --save-dev @angular/cli@latest


#angular 
 0. ng version
 1. ng new angular-app
 2. ng g components comp-name



#mysql
ubuntu에 mysql 깔고 
#외부 접속 권한 만들기
ALTER USER 'pocachip'@'%' IDENTIFIED WITH mysql_native_password by 'media2015!';
CREATE USER 'pocachip'@'%' IDENTIFIED BY 'media2015!';
GRANT ALL PRIVILEGES ON *.* to 'pocachip'@'%';
flush privileges;

# 데이타 옮기기
1. mysql workbench data export
2. window explorer files copy -> 원격 컴퓨터 files paste
3. mysql workbench data import 

cp result_mvo.son test.json
sed -i '/^\[/d' test.json
sed -i '/^\]/d' test.json
sed -i '/^$/d' test.json
sed 's/,$//g' test.json >test_out.json
tr -d '\n' < test_out.json > test_online.json

#jq validate json
cat test_online.json | jq .

MySQL shell 
\c mysqlx://root:dmscks3927!(server: media123! companypc: dmstn3927!)@localhost
\use rightwatch
util.importJson("c:\\test_online.json", {schema: "rightwatch", table:"tmp_post",tableColumn: "json"});
# 콘텐츠별 체크리스트 order by 
select * from (select a.id, a.title, count(*) as tc from kta_contents as a left join check_list as b on a.id = b.content_id group by a.id) as c order by tc desc;

# 중복 확인 및 제거 방법
-- 중복 데이터 찾기
SELECT  title ,  -- 중복되는 데이터
         COUNT(title) -- 중복 갯수
FROM kta_contents              -- 중복조사를 할 테이블 이름
GROUP BY title      -- 중복되는 항목 조사를 할 컬럼
HAVING COUNT(title) > 1 ;  -- 1개 이상 (갯수)

-- 중복 데이터 삭제
delete t1 from kta_contents t1 join kta_contents t2 on t1.title=t2.title where t1.id > t2.id;

# insert content_list2
CREATE TABLE `kta_contents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `genre` varchar(256) DEFAULT NULL,
  `title` varchar(256) DEFAULT NULL,
  `actors` TEXT DEFAULT NULL,
  `director` varchar(256) DEFAULT NULL,
  `price` varchar(256) DEFAULT NULL,
  `enddate` varchar(256) DEFAULT NULL,
  `synop` TEXT DEFAULT NULL,
  `p_url` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4353 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO kta_contents(genre, title, actors, director, price, enddate, synop)  
SELECT json->> '$."genre"',
json->> '$."title"',
json->> '$."actors"',
json->> '$."director"',
json->> '$."price"',
json->> '$."enddate"',
json->> '$."synop"'
FROM tmp_post;

# insert content_list
INSERT INTO contents_list(title)  SELECT json->> '$."title"' FROM tmp_post

CREATE  TABLE rightwatch.post ( 
	id                   INT AUTO_INCREMENT PRIMARY KEY,
	website              INT  NOT NULL     ,
	cat1_code            VARCHAR(10)       ,
	cat2_code            VARCHAR(10)       ,
	cat1_title           VARCHAR(30)       ,
	cat2_title           VARCHAR(30)       ,
	idx                  VARCHAR(256)    ,
	txt                  VARCHAR(256)       ,
	lvl19                VARCHAR(10)       ,
	payment                VARCHAR(10)       ,
	seller               VARCHAR(256)       ,
	partnership              VARCHAR(16)       ,
	attach_file_size     VARCHAR(256)       ,
	item_url     VARCHAR(256)       ,
	last_update          VARCHAR(256)     
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

use rightwatch;
insert into post(id, website, cat1_code, cat2_code, cat1_title ,cat2_title       
,idx ,txt ,lvl19, price, seller, partner, attach_file_size, item_url
,last_update)
select 
    null,
	json->>'$.website',
	json->>'$.cat1_code',
	json->>'$.cat2_code',
	json->>'$.category_title',
	json->>'$.sub_category_title',
	json->>'$.idx',
	json->>'$.txt',
	json->>'$.Lvl19',
	json->>'$.point',
	json->>'$.seller',
	json->>'$.partner',
	json->>'$.attach_file_size',
    json->>'$.item_url',
	json->>'$.time'
from rightwatch.tmp_post

#ginbro
ginbro gen -u root -p dmscks3927! -a "127.0.0.1:3306" -d rightwatch -c utf8 -o=rightwatch
go mod init
go mod tidy
go build
rightwatch.exe

#ngx-admin
npm start


#github
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
git config --global user.name "pocachip"
git config --global user.email "parkseou@gmail.com"
git rm --cached . -rf 

git status
git add .
git commit -m "add ..."
git push



select * from (select a.id, a.title, count(*) as tc from kta_contents as a left join check_list as b on a.id = b.content_id group by a.id) as c order by tc desc;

#SubQuery
db.Where("amount > (?)", db.Table("orders").Select("AVG(amount)")).Find(&orders)
// SELECT * FROM "orders" WHERE amount > (SELECT AVG(amount) FROM "orders");

subQuery := db.Select("AVG(age)").Where("name LIKE ?", "name%").Table("users")
db.Select("AVG(age) as avgage").Group("name").Having("AVG(age) > (?)", subQuery).Find(&results)
// SELECT AVG(age) as avgage FROM `users` GROUP BY `name` HAVING AVG(age) > (SELECT AVG(age) FROM `users` WHERE name LIKE "name%")


#from sub query
db.Table("(?) as u", db.Model(&User{}).Select("name", "age")).Where("age = ?", 18).Find(&User{})
// SELECT * FROM (SELECT `name`,`age` FROM `users`) as u WHERE `age` = 18

subQuery1 := db.Model(&User{}).Select("name")
subQuery2 := db.Model(&Pet{}).Select("name")
db.Table("(?) as u, (?) as p", subQuery1, subQuery2).Find(&User{})
// SELECT * FROM (SELECT `name` FROM `users`) as u, (SELECT `name` FROM `pets`) as p


db.Joins("JOIN emails ON emails.user_id = users.id AND emails.email = ?", "jinzhu@example.org").Find(&user)

subQuery := db.Model(&kta_content{}).Select("id, title, count(*) as tc").Joins("left join check_list on kta_content.id=check_list.id).Group("id")
db.Table("(?) as u", subQuery  ).Order(tc desc).find(&kta_content{})

# Crawler
1. venv activate
2. scrapy crawl ondisk_p -o result.json -a category=MVO sub_sec=MVO_002  //multi arguemnt pass
   --need to fix don't count bbs if it has command arguments...
3. mysql 연동
pip3 install mysql-connector-python

ondisk_spider.py : full scan with file output, it need settings.py without pipelines.py / spider name: ondisk_po
ondisk_spider2.py : update scan without file output, it need settings.py with pipelines.py / spider name: ondisk_update


# docker
1. docker -v   (windows power shell)
2. docker pull mysql 
3. docker images
4. docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=<password> -d -p 3306:3306 mysql:latest
5. 
	# MySQL Docker 컨테이너 중지
	$ docker stop mysql-container

	# MySQL Docker 컨테이너 시작
	$ docker start mysql-container

	# MySQL Docker 컨테이너 재시작
	$ docker restart mysql-container
6. 접속
$ docker exec -it mysql-container1 bash
