this is my next project (by pocachip 2023-10-17)
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

#ngx-admin은 
nvm ls-remote
1.install node 14.21.3
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
cp result_mvo.json test.json
sed -i '/^\[/d' test.json
sed -i '/^\]/d' test.json
sed -i '/^$/d' test.json
sed 's/,$//g' test.json >test_out.json
tr -d '\n' < test_out.json > test_online.json


MySQL shell 
\c mysqlx://root:dmscks3927!@localhost
\use rightwatch
util.importJson("c:\\test_online.json", {schema: "rightwatch", table:"tmp_post",tableColumn: "json"});
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



