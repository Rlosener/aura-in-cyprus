<?php

declare(strict_types=1);

header('Content-Type: text/plain; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    header('Allow: POST');
    echo 'Bu form yalnızca POST isteklerini kabul eder.';
    exit;
}

function aura_form_value(string $key): string
{
    $value = $_POST[$key] ?? '';
    if (!is_string($value)) {
        return '';
    }

    return trim(str_replace(["\r", "\n"], ' ', strip_tags($value)));
}

$name = aura_form_value('name');
$email = filter_var(aura_form_value('email'), FILTER_SANITIZE_EMAIL);
$subject = aura_form_value('subject');
$number = aura_form_value('number');
$message = trim(strip_tags((string) ($_POST['message'] ?? '')));
$recipient = filter_var(getenv('AURA_CONTACT_EMAIL') ?: '', FILTER_VALIDATE_EMAIL);

if (
    $name === ''
    || $subject === ''
    || $number === ''
    || $message === ''
    || !filter_var($email, FILTER_VALIDATE_EMAIL)
) {
    http_response_code(422);
    echo 'Lütfen ad, e-posta, telefon, konu ve mesaj alanlarını eksiksiz doldurun.';
    exit;
}

if ($recipient === false) {
    http_response_code(503);
    echo 'İletişim formu henüz yapılandırılmadı. Lütfen daha sonra yeniden deneyin.';
    exit;
}

$mailSubject = 'Aura In Cyprus iletişim talebi: ' . $subject;
$emailContent = "Ad Soyad: {$name}\n";
$emailContent .= "Konu: {$subject}\n";
$emailContent .= "E-posta: {$email}\n";
$emailContent .= "Telefon: {$number}\n\n";
$emailContent .= "Mesaj:\n{$message}\n";
$headers = [
    'From: Aura In Cyprus Web Sitesi <' . $recipient . '>',
    'Reply-To: ' . $name . ' <' . $email . '>',
    'Content-Type: text/plain; charset=UTF-8',
];

if (mail($recipient, $mailSubject, $emailContent, implode("\r\n", $headers))) {
    http_response_code(200);
    echo 'Teşekkürler. Mesajınız Aura In Cyprus ekibine iletildi.';
    exit;
}

http_response_code(500);
echo 'Mesajınız şu anda gönderilemedi. Lütfen daha sonra yeniden deneyin.';
