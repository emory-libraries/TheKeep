#!/usr/bin/php -q

<?
/**
 * *****************************************************************************
 *
 * *****************************************************************************
**/ 

echo "start \n";
	require_once('DB.php');

    $dsn = array(
        'phptype'  => 'pgsql',
        'username' => 'digmast_user',
        'password' => 'emory30322',
        'hostspec' => 'localhost',
        'database' => 'digital_masters'
    );

    $options = array(
        'ssl'       => 'true',
        'debug'     => 'true'
    );
    
    $g_dbConn =& DB::connect($dsn, $options);
    if (DB::isError($g_dbConn)) { echo ($g_dbConn->getMessage().' - '.$g_dbConn->getUserinfo()); }
    
echo "connection open\n";    
    
    $sql['getTI'] = "SELECT id, content_id FROM tech_sounds where content_id is not null";
    $sql['getSI'] = $g_dbConn->prepare('SELECT id FROM src_sounds where content_id = !');
    $sql['update'] = $g_dbConn->prepare("UPDATE tech_sounds SET src_sound_id = ! where id = !");
    
echo "statements prepared\n";    
    
    
    
    $rs_ti =& $g_dbConn->query($sql['getTI']);
	if (PEAR::isError($rs_ti)) { echo ($rs_ti->getMessage().' - '.$rs_ti->getUserinfo()); }

echo "TI data retrieved\n";	
	
	while (($row = $rs_ti->fetchRow(DB_FETCHMODE_ASSOC)) != FALSE)
	{
echo " content_id = " . $row['content_id'];		
		$rs_src_img =& $g_dbConn->execute($sql['getSI'], $row['content_id']);

		$src_row = $rs_src_img->fetchRow(DB_FETCHMODE_ASSOC);
		
		echo " src_id = " . $src_row['id'] . " id = " . $row['id'] . "\n";
		
		$g_dbConn->execute($sql['update'], array($src_row['id'], $row['id']));
	}
