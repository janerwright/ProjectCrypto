<?php 
require 'PHPMailerAutoload.php';
if(isset($_POST['send_message'])){
  $to = 'learn.cyber@outlook.com';
  $from = 'From: Learn Cyber';
  $subject = 'Website Form Submission';
  $message = 'Name: ' . $_POST['forename'] . "\r\n\r\n";
  $message = 'Email: ' . $_POST['email'] . "\r\n\r\n";
  $message = 'Message: ' . $_POST['msg'];
  mail($to, $subject, $message);
  header('Location: ../index.html');
}

if ($_POST['send_message']) {
    if (mail ($to, $subject, $message, $from)) { 
        echo '<p>Your message has been sent!</p>';
    } else { 
        echo '<p>Something went wrong, go back and try again!</p>'; 
    }
}
?>