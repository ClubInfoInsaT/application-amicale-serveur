<?php
require_once 'dao.php';

$password = "df1g3f1ghdf54qds3f879";

$rest_json = file_get_contents("php://input");
$_POST = json_decode($rest_json, true);

if (!isset($_POST['password']) || isset($_POST['password']) != $password)
    die("Access denied");


if (isset($_POST['function'])) {
    if ($_POST['function'] == "setup_machine_notification")
        setup_machine_notification();
    elseif ($_POST['function'] == "get_machine_watchlist")
        get_machine_watchlist();
    elseif ($_POST['function'] == "set_machine_reminder")
        set_machine_reminder();
} else
    show_error();

function setup_machine_notification() {
    $token = $_POST['token'];
    $enabled = boolval($_POST['enabled']);
    $machineId = intval($_POST['machine_id']);
    $locale = $_POST['locale'];

    $dao = new Dao();
    $dao->update_machine_end_token($token, $machineId, $enabled, $locale);
}

function get_machine_watchlist() {
    $token = $_POST['token'];

    $dao = new Dao();
    echo json_encode($dao->get_machine_watchlist($token));
}

function set_machine_reminder() {
    $token = $_POST['token'];
    $time = intval($_POST['time']);

    $dao = new Dao();
    $dao->set_machine_reminder($token, $time);
}


function show_error() {
    echo "Échec :\n";
    var_dump($_POST);
}
