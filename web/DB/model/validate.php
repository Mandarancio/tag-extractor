<?php
//update if image correctly classified or not

//get data from ajax query; 
//data: id_categ ; id_pict ; value_of_the_radio_button
//update is_right column from picture_category_link table 

class MyDB extends SQLite3
{
    function __construct()
    {
        $this->open('../output-classified.db');
    }
}

$db = new MyDB();
//exemple update query
// $db->exec('UPDATE picture_category_link SET is_right = 1 WHERE picture_category_link.picture_id=1 and picture_category_link.category_id= 1');
?>