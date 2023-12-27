CREATE DEFINER=`root`@`localhost` PROCEDURE `create_check_contents`(
   -- parameter
   c_id VARCHAR(20)
   )
BEGIN
	DECLARE srch_str VARCHAR(128);
    DECLARE postid VARCHAR(128);
    DECLARE postidx VARCHAR(256);
    DECLARE posttxt VARCHAR(128);

	IF (select count(*) from check_list where content_id = c_id) > 0 THEN
     select 'alread have check list';
	 delete from check_list where content_id = c_id;
	END IF;

	-- query2
INSERT into check_list(content_id,post_id, post_idx, post_txt)        
SELECT c_id, id, idx, txt 
        into postid, postidx, posttxt
        from post 
		where match(txt)
        against ((select title from contents_list where id = c_id) IN NATURAL LANGUAGE MODE);
END

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_check_all`()
BEGIN
  DECLARE done BOOLEAN DEFAULT FALSE;
  DECLARE _id BIGINT UNSIGNED;
  DECLARE cur CURSOR FOR SELECT id FROM kta_contents;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done := TRUE;

  OPEN cur;

  testLoop: LOOP
    FETCH cur INTO _id;
    IF done THEN
      LEAVE testLoop;
    END IF;    
    CALL check_contents(_id);
  END LOOP testLoop;

  CLOSE cur;
END

CREATE DEFINER=`root`@`localhost` PROCEDURE `check_contents`(
   -- parameter
   c_id VARCHAR(20)
)
BEGIN
  DECLARE srch_str VARCHAR(128);
  DECLARE contentid VARCHAR(128);
  DECLARE postid VARCHAR(128);
  DECLARE postidx VARCHAR(256);
  DECLARE posttxt VARCHAR(128);
  DECLARE done BOOLEAN DEFAULT FALSE;
  DECLARE _id BIGINT UNSIGNED;
  DECLARE score BIGINT UNSIGNED;
  DECLARE cur1 CURSOR FOR SELECT id, idx, txt, match(txt) against((select concat('+',title) from kta_contents where id = c_id) IN NATURAL LANGUAGE MODE) as scorein
                from post 
		where match(txt)
        against ((select concat('+',title) from kta_contents where id = c_id) IN NATURAL LANGUAGE MODE)
        having scorein > 0
        order by scorein asc
        limit 0, 5;
  DECLARE cur CURSOR FOR SELECT id, idx, txt from post where txt like (select concat("%", title, "%") from kta_contents where id = c_id);
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done := TRUE;
  
  OPEN cur;
  
  testLoop: LOOP
	FETCH cur INTO postid, postidx, posttxt;    
    IF done THEN
      LEAVE testLoop;
    END IF;    

    IF (select count(*) from check_list where content_id = c_id and post_id = postid) = 0 THEN
		INSERT into check_list(content_id,post_id, post_idx, post_txt) values (c_id, postid, postidx, posttxt);
    END IF;    
  END LOOP testLoop;

  CLOSE cur;  
END