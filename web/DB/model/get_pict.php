<?php

class MyDB extends SQLite3
{
    function __construct()
    {
        $this->open('../output-classified.db');
    }
}

$db = new MyDB();

$result = $db->query("SELECT picture.id as id, picture.lat as lat, picture.lon as lng, picture.image_url as url, tag.tag as tag, category.name as cat_name
					  FROM picture, tag, picture_tag_link, category, picture_category_link
					  WHERE picture.id=picture_tag_link.picture_id 
							AND tag.id=picture_tag_link.tag_id 
							AND picture.id=picture_category_link.picture_id 
							AND category.id=picture_category_link.category_id");
$data=array();
while ($row = $result->fetchArray()) 
{
	$pos=$row['lat'].'_'.$row['lng'];
    if(! array_key_exists($pos, $data))
	{
		$data[$pos]=array('lat' 	=>$row['lat'],
						  'lng'		=>$row['lng'],
						  'pict'	=>array(),
		);
	}
	
	if(! array_key_exists($row['id'], $data[$pos]['pict']))
	{
		$data[$pos]['pict'][$row['id']]=array('url'			=>$row['url'],
											  'categorie'	=>$row['cat_name'],
											  'tag' 		=> ''
		);
	}
	
	if((in_array($row['cat_name'], $data[$pos]['pict'][$row['id']])) &&  $row['tag']!="")
	{
		$data[$pos]['pict'][$row['id']]['tag']=$data[$pos]['pict'][$row['id']]['tag'].' #'.$row['tag'];
	}
}
$json_data=json_encode($data, JSON_UNESCAPED_UNICODE);
echo $json_data;
?>