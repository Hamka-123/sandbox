<?php
// --- АВТОРИЗАЦИЯ (Harsha'ot) ---
$user = 'admin';
$pass = 'K#9p!vL2_mZ6*sQn8Rxt';

if (!isset($_SERVER['PHP_AUTH_USER']) || $_SERVER['PHP_AUTH_USER'] !== $user || $_SERVER['PHP_AUTH_PW'] !== $pass) {
    header('WWW-Authenticate: Basic realm="Slaweb Ultimate Audit"');
    header('HTTP/1.0 401 Unauthorized');
    die("Доступ ограничен");
}

// --- СБОР ДАННЫХ (Bli Harsha'ot Root) ---

// 1. Система и Uptime
$os_data = @parse_ini_file('/etc/os-release');
$os_name = $os_data['PRETTY_NAME'] ?? 'Ubuntu 18.04';
$uptime = shell_exec('uptime -p');
$load = sys_getloadavg();

// 2. Ресурсы (Диск и Иноды)
$inode_usage = (int)shell_exec("df -i / | awk '{print $5}' | tail -1 | sed 's/%//'");
$disk_usage = (int)shell_exec("df / | awk '{print $5}' | tail -1 | sed 's/%//'");
$disk_free = shell_exec("df -h / | awk '{print $4}' | tail -1");

// 3. Память (Zichron)
$free_out = shell_exec('free');
$free_lines = explode("\n", trim($free_out));
$mem = preg_split('/\s+/', $free_lines[1]);
$swp = preg_split('/\s+/', $free_lines[2]);
$mem_pct = round($mem[2] / $mem[1] * 100);
$swp_pct = $swp[1] > 0 ? round($swp[2] / $swp[1] * 100) : 0;

// 4. SSL МОНИТОРИНГ (Tikun Ta'ut - Исправлено)
$domain = $_SERVER['HTTP_HOST'];
$days_left = "ERR";
$update_date = "Auto";

// Попытка 1: Через сетевой сокет (самый надежный)
$get_ssl_context = stream_context_create(["ssl" => ["capture_peer_cert" => true, "verify_peer" => false, "verify_peer_name" => false]]);
$read_ssl = @stream_socket_client("ssl://$domain:443", $errno, $errstr, 2, STREAM_CLIENT_CONNECT, $get_ssl_context);

if ($read_ssl) {
    $params = stream_context_get_params($read_ssl);
    $cert = openssl_x509_parse($params["options"]["ssl"]["peer_certificate"]);
    $days_left = round(($cert['validTo_time_t'] - time()) / 86400);
    fclose($read_ssl);
} else {
    // Попытка 2: Локальная проверка через openssl
    $ssl_cmd = "timeout 2s openssl s_client -connect 127.0.0.1:443 -servername $domain </dev/null 2>/dev/null | openssl x509 -noout -dates";
    $ssl_info = shell_exec($ssl_cmd);
    if (preg_match('/notAfter=(.*)/', $ssl_info, $matches)) {
        $days_left = round((strtotime($matches[1]) - time()) / 86400);
    }
}

// Попытка найти дату обновления файла (Let's Encrypt)
$cert_path = "/etc/letsencrypt/live/$domain/fullchain.pem";
if (@file_exists($cert_path)) {
    $update_date = date("d.m.Y", filemtime($cert_path));
}

// 5. Сетевой трафик (Ta'avora)
$net_data = shell_exec("cat /proc/net/dev | grep -E 'eth0|ens3|enp|eno' | head -n 1");
$net_parts = preg_split('/\s+/', trim($net_data));
$received_gb = isset($net_parts[1]) ? round($net_parts[1] / 1073741824, 2) : 0;
$sent_gb = isset($net_parts[9]) ? round($net_parts[9] / 1073741824, 2) : 0;

// 6. Активность (Chiburim)
$visitors = (int)shell_exec("netstat -an | grep :443 | grep ESTABLISHED | wc -l");
$php_procs = (int)shell_exec("ps aux | grep -c 'php-fpm\|apache2'");

// Вспомогательные функции
function check_service($port) {
    $fp = @fsockopen('127.0.0.1', $port, $errno, $errstr, 0.2);
    if ($fp) { fclose($fp); return "OK"; }
    return "DOWN";
}

function get_status_color($val, $crit, $rev = false) {
    if ($val === "ERR" || $val <= 0 && $rev) return "#ff4d4d";
    if ($rev) return $val < $crit ? "#ff4d4d" : "#4caf50";
    return $val > $crit ? "#ff4d4d" : "#4caf50";
}
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Slaweb Ultimate Monitor</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0c0c0c; color: #e0e0e0; padding: 20px; margin: 0; }
        .container { max-width: 1100px; margin: 0 auto; }
        .header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 25px; border-bottom: 1px solid #222; padding-bottom: 15px; }
        .os-badge { background: #00d4ff; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85em; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 15px; }
        .card { background: #161616; padding: 20px; border-radius: 12px; border-top: 5px solid #444; position: relative; }
        
        .label { font-size: 0.7em; text-transform: uppercase; color: #888; letter-spacing: 1px; }
        .value { font-size: 2.3em; font-weight: bold; margin: 10px 0; color: #fff; }
        .sub { font-size: 0.85em; color: #666; }
        
        .progress-bg { height: 4px; background: #222; margin-top: 15px; border-radius: 2px; }
        .progress-fill { height: 100%; border-radius: 2px; transition: width 0.8s ease-in-out; }
        
        .footer { margin-top: 40px; text-align: center; color: #333; font-size: 0.8em; border-top: 1px solid #222; padding-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1 style="margin:0;">🩺 Health Check: <?= shell_exec('hostname') ?></h1>
                <div class="sub" style="margin-top:5px;">
                    Система: <span class="os-badge"><?= $os_name ?></span> | <?= $uptime ?>
                </div>
            </div>
            <div style="text-align:right" class="sub">
                LA: <?= $load[0] ?> | <?= $load[1] ?> | <?= $load[2] ?>
            </div>
        </div>

        <div class="grid">
            <div class="card" style="border-top-color: <?= get_status_color($disk_usage, 85) ?>">
                <div class="label">Диск и Иноды</div>
                <div class="value"><?= $disk_usage ?>% / <?= $inode_usage ?>%</div>
                <div class="sub">Свободно: <?= $disk_free ?></div>
                <div class="progress-bg"><div class="progress-fill" style="width:<?= $disk_usage ?>%; background:<?= get_status_color($disk_usage, 85) ?>"></div></div>
            </div>

            <div class="card" style="border-top-color: <?= get_status_color($mem_pct, 80) ?>">
                <div class="label">Память (RAM)</div>
                <div class="value"><?= $mem_pct ?>%</div>
                <div class="sub">Swap usage: <?= $swp_pct ?>%</div>
                <div class="progress-bg"><div class="progress-fill" style="width:<?= $mem_pct ?>%; background:<?= get_status_color($mem_pct, 80) ?>"></div></div>
            </div>

            <div class="card" style="border-top-color: <?= get_status_color($days_left, 14, true) ?>">
                <div class="label">SSL Безопасность</div>
                <div class="value"><?= $days_left === "ERR" ? "ERR" : $days_left . " дн." ?></div>
                <div class="sub">Обновлено: <?= $update_date ?></div>
            </div>

            <div class="card" style="border-top-color: #ff9800">
                <div class="label">Сетевой трафик</div>
                <div class="value"><?= $received_gb ?> <small style="font-size:0.5em">GB</small></div>
                <div class="sub">In. Out: <?= $sent_gb ?> GB</div>
            </div>

            <div class="card" style="border-top-color: #00bcd4">
                <div class="label">Соединения (HTTPS)</div>
                <div class="value"><?= $visitors ?></div>
                <div class="sub">Уникальных IP онлайн</div>
            </div>

            <div class="card" style="border-top-color: #9c27b0">
                <div class="label">Доступность портов</div>
                <div class="sub" style="margin-top:10px; line-height:1.8;">
                    MySQL (3306): <b style="color:#fff"><?= check_service(3306) ?></b><br>
                    Apache (80): <b style="color:#fff"><?= check_service(80) ?></b><br>
                    PHP Procs: <b style="color:#fff"><?= $php_procs ?></b>
                </div>
            </div>
        </div>

        <div class="footer">
            Обновлено: <?= date('d.m.Y H:i:s') ?> | PHP v<?= PHP_VERSION ?> | Сделано с 💙 для Slaweb
        </div>
    </div>
</body>
</html>