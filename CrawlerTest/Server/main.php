<?php
/*
 *Package  : crawler test in server
 *Function : 服务器端用于测试爬虫
 *Author   : bihuchao <bihuchao1995@gmail.com>
 */
if($_POST){
    printf("POST:\n");
    foreach ($_POST as $key => $value)
        printf("    %s %s\n", $key, $value);
}
if($_GET){
    printf("GET:\n");
    foreach ($_GET as $key => $value)
        printf("    %s %s\n", $key, $value);
}

    
