<?php
/**
 * VALENIZED — Contact form handler
 * File location: /public_html/contact.php
 *
 * Configure: edit the two constants below (TO_EMAIL, FROM_EMAIL).
 * Upload all site files & this PHP into Hostinger's public_html/.
 * Hostinger servers have PHP mail() pre-configured.
 *
 * Returns JSON: { ok: bool, error?: string }
 *
 * Honeypot field "_gotcha" must be empty; if filled, the request is
 * silently dropped (anti-spam).
 */

declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');

const TO_EMAIL   = 'inquire@valenized.com';   // ← where leads land
const FROM_EMAIL = 'no-reply@valenized.com';  // ← must be on your domain
const SITE_NAME  = 'VALENIZED';

/* ---------- helpers ---------- */
function fail(string $msg, int $code = 400): void {
    http_response_code($code);
    echo json_encode(['ok' => false, 'error' => $msg]);
    exit;
}
function clean(string $v): string {
    return trim(str_replace(["\r", "\n"], ' ', $v));
}

/* ---------- method check ---------- */
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    fail('Method not allowed', 405);
}

/* ---------- honeypot ---------- */
if (!empty($_POST['_gotcha'])) {
    // pretend it worked to the bot
    echo json_encode(['ok' => true]);
    exit;
}

/* ---------- read fields ---------- */
$name        = clean($_POST['name']        ?? '');
$company     = clean($_POST['company']     ?? '');
$email       = clean($_POST['email']       ?? '');
$discipline  = clean($_POST['discipline']  ?? '');
$budget      = clean($_POST['budget']      ?? '');
$brief       = trim($_POST['brief']        ?? '');

/* ---------- validate ---------- */
$errors = [];
if ($name === '' || mb_strlen($name) < 2)        $errors[] = 'name';
if (!filter_var($email, FILTER_VALIDATE_EMAIL))   $errors[] = 'email';
if ($brief === '' || mb_strlen($brief) < 10)      $errors[] = 'brief';

if (!empty($errors)) {
    fail('missing or invalid: ' . implode(', ', $errors));
}

/* ---------- compose email ---------- */
$ip    = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$ua    = $_SERVER['HTTP_USER_AGENT'] ?? 'unknown';
$when  = date('Y-m-d H:i:s e');

$subject = sprintf('[%s] %s — %s',
    $budget ?: 'no-budget',
    $name,
    $company !== '' ? $company : 'walk-up'
);

$body  = "New brief received via valenized.com\n\n";
$body .= "When       : {$when}\n";
$body .= "Name       : {$name}\n";
$body .= "Company    : {$company}\n";
$body .= "Email      : {$email}\n";
$body .= "Discipline : {$discipline}\n";
$body .= "Budget     : {$budget}\n";
$body .= "IP / UA    : {$ip} / {$ua}\n";
$body .= "-------------------------------------------\n\n";
$body .= "Brief:\n{$brief}\n";

/* multipart headers */
$boundary = md5((string)microtime(true));
$headers  = [];
$headers[] = "From: " . SITE_NAME . " <" . FROM_EMAIL . ">";
$headers[] = "Reply-To: {$name} <{$email}>";
$headers[] = "MIME-Version: 1.0";
$headers[] = "Content-Type: text/plain; charset=UTF-8";
$headers[] = "X-Mailer: VALENIZED-contact.php";
$headerStr = implode("\r\n", $headers);

/* ---------- send ---------- */
$sent = @mail(TO_EMAIL, $subject, $body, $headerStr);

/* ---------- log fallback (always) ---------- */
$logDir  = __DIR__ . '/logs';
$logFile = $logDir . '/submissions.log';
@mkdir($logDir, 0755, true);
@file_put_contents(
    $logFile,
    sprintf("[%s] mail()=%s\n%s\n\n", $when, $sent ? 'OK' : 'FAIL', $body),
    FILE_APPEND
);

if (!$sent) {
    // Mail didn't go through, but log did — still 200 so JS sees ok
    // You will see it in the dashboard via the log file.
}

echo json_encode(['ok' => true]);
