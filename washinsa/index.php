<?php
/**
 * Wash-INSA PARSER
 * This program get all information about the laundry
 * Author : Gabin NOBLET (Promo 55)
 * Date : 07/2019
 * Version 1.0
 */


/**Get Type of machines (1 for dryers, 2 for washers, 0 else)
 * @param $str (string)
 * @return int
 */
function mType($str)
{
    $a = explode(' ', $str);
    if (substr($a[0], -5) == "SECHE") {
        return 1;
    } elseif (substr($a[0], -4) == "LAVE") {
        return 2;
    } else {
        return 0;
    }
}

/**Get Status of machines (1 for available, 2 for current, 3 for finished, 0 for out of order)
 * @param $node (DOMNode)
 * @return int
 */
function mStatus($node)
{
    $a = explode(' ', $node[2]->nodeValue);
    if (substr($a[0], -10) == "DISPONIBLE") {
        return 1;
    } elseif (substr($a[0], -7) == "TERMINE") {
        return 3;
    } elseif (isset($node[4])) {   //If there is time information, it is current
        return 2;
    } else {
        return 0;
    }
}

/** Clean strings (removes spaces, tabs end return before and behind the string)
 * @param $str (string)
 * @return string
 */
function clean($str)
{
    return rtrim(ltrim(htmlspecialchars_decode($str)));
}


function generateJson()
{
    $page = new DOMDocument();
    $page->loadHTMLFile("https://www.proxiwash.com/weblaverie/ma-laverie-2?s=cf4f39&16d33a57b3fb9a05d4da88969c71de74=1"); //Get page


    $division = $page->getElementById("liste-machines");
    $liste_machines = $division->childNodes[0]->childNodes;

//Remove titles
    $titles = $liste_machines->item(0);
    $titles->parentNode->removeChild($titles);


    $return = array(
        'dryers' => array(),
        'washers' => array()
    );

    foreach ($liste_machines as $machines) {

        $specs = $machines->childNodes;

        //Format array
        $template = array(
            'number' => "",
            'state' => "",
            'startTime' => "",
            'endTime' => "",
            'donePercent' => "",
            'remainingTime' => ""
        );

        //Get info from HTML
        $specsArray = array();
        foreach ($specs as $info) {
            if (isset($info->tagName)) {
                if ($info->tagName == "td") {
                    array_push($specsArray, $info);
                }
            }
        }

        //Get Type
        $type = mType(clean($specsArray[0]->nodeValue));

        //Get Number
        preg_match('/\d{1,2}/', $specsArray[1]->nodeValue, $number);
        $template['number'] = $number[0];

        //Get Status and DonePercent
        $status = mStatus($specsArray);
        switch ($status) {
            case 1:
                $template['state'] = "DISPONIBLE";
                break;
            case 2:
                $template['state'] = "EN COURS";
                foreach ($specsArray[2]->childNodes as $child) {
                    if (isset($child->tagName)) {
                        if ($child->tagName == "table") {
                            $progressBar = $child->childNodes[0]->childNodes[0];
                            if ($progressBar->getAttribute('bgcolor') == "Green") {
                                $template['donePercent'] = substr($progressBar->getAttribute('width'), 0, -1);
                            }
                        }
                    }
                }
                break;
            case 3:
                $template['state'] = "TERMINE";
                break;
            default :
                $template['state'] = "HORS SERVICE";
                break;
        }

        if ($template['state'] === "EN COURS") { // We set Times only when they could exist
            //Get StartTime
            $template['startTime'] = $specsArray[4]->nodeValue;
            //Get EndTime
            $template['endTime'] = $specsArray[5]->nodeValue;
            $template['remainingTime'] = get_remaining_time($template['startTime'], $template['endTime'], $template['donePercent']);
        }

        if ($type == 1) {
            array_push($return['dryers'], $template);
        } elseif ($type == 2) {
            array_push($return['washers'], $template);
        }

//    echo "<pre>";
//    echo "Type : ".$type."\n" ;
//    print_r($template);
//    echo "</pre>";
    }
    $jsonData = json_encode($return);
    file_put_contents('washinsa.json', $jsonData);
}


/**
 * Get remaining time for the current machine
 *
 * @param $startTime
 * @param $endTime
 * @return string
 */
function get_remaining_time($startTime, $endTime, $percentDone)
{
    $startArray = explode(':', $startTime);
    $endArray = explode(':', $endTime);

    $unixStart = mktime($startArray[0], $startArray[1], 0, 1, 0);
    $unixEnd = mktime($endArray[0], $endArray[1], 0, 1, 0);

    if ($unixStart > $unixEnd) { // Machine ends the following day
        $unixEnd = mktime($endArray[0], $endArray[1], 0, 1, 1);
    }
    $deltaMinutes = ($unixEnd - $unixStart)/60;
    $remainingTime = $deltaMinutes * (1 - $percentDone/100);
    return strval(round($remainingTime, 0));
}

generateJson();
