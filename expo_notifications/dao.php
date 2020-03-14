<?php

class Dao
{
    private $conn;
    private $debug = false;

    private function get_debug_mode()
    {
        $this->debug = file_exists(__DIR__ . DIRECTORY_SEPARATOR . "DEBUG");
    }


    public function __construct()
    {
        $this->get_debug_mode();
        if ($this->debug) {
            $username = 'test';
            $password = $this->read_password();;
            $dsn = 'mysql:dbname=test;host=127.0.0.1';
        } else {
            $username = 'amicale_app';
            $password = $this->read_password();
            $dsn = 'mysql:dbname=amicale_app;host=127.0.0.1';
        }
        try {
            $this->conn = new PDO($dsn, $username, $password, [PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8']);
        } catch (PDOException $e) {
            echo $e;
        }
    }

    private function read_password()
    {
        if ($this->debug)
            $real_path = __DIR__ . DIRECTORY_SEPARATOR . ".htpassdb_debug";
        else
            $real_path = __DIR__ . DIRECTORY_SEPARATOR . ".htpassdb";
        $file = fopen($real_path, "r") or die("Unable to open DB password file!");;
        $password = fgets($file);
        fclose($file);
        return trim($password);
    }

    /**
     * Return the list of machines watched by the user associated by the given token
     *
     * @param $token
     * @return array
     */
    public function get_machine_watchlist($token) {
        $this->register_user($token);
        $sql = "SELECT machine_id FROM machine_watchlist WHERE user_token=:token";
        $cursor = $this->conn->prepare($sql); // Protect against SQL injections
        $cursor->bindParam(':token', $token);
        $cursor->execute();
        $result = $cursor->fetchAll();
        $finalArray = [];
        foreach ($result  as $row) {
            array_push($finalArray, $row["machine_id"]);
        }
        return $finalArray;
    }


    public function set_machine_reminder($token, $time) {
        $this->register_user($token);
        $sql = "UPDATE users SET machine_reminder_time=:time WHERE token=:token";
        $cursor = $this->conn->prepare($sql); // Protect against SQL injections
        $cursor->bindParam(':token', $token);
        $cursor->bindParam(':time', $time);
        var_dump($cursor->execute());
    }


    /**
     * Add/Remove a machine from the database for the specified token.
     *
     * @param $token
     * @param $machine_id
     * @param $should_add
     */
    public function update_machine_end_token($token, $machine_id, $should_add, $locale)
    {
        $this->register_user($token);
        $this->update_user_locale($token, $locale);
        if ($should_add)
            $sql = "INSERT INTO machine_watchlist (machine_id, user_token) VALUES (:id, :token)";
        else
            $sql = "DELETE FROM machine_watchlist WHERE machine_id=:id AND user_token=:token";
        $cursor = $this->conn->prepare($sql); // Protect against SQL injections
        $cursor->bindParam(':id', $machine_id);
        $cursor->bindParam(':token', $token);
        $cursor->execute();
    }


    /**
     * Register user in the database if not already in it
     * @param $userToken
     * @param $locale
     */
    private function register_user($userToken) {
        $sql = "INSERT INTO users (token) VALUES (:token)";
        $cursor = $this->conn->prepare($sql); // Protect against SQL injections
        $cursor->bindParam(':token', $userToken);
        $cursor->execute();
    }

    private function update_user_locale($token, $locale) {
        $sql = "UPDATE users SET locale=:locale WHERE token=:token";
        $cursor = $this->conn->prepare($sql); // Protect against SQL injections
        $cursor->bindParam(':token', $token);
        $cursor->bindParam(':locale', $locale);
        $cursor->execute();
    }

}


