#!/usr/bin/perl

#este script esta metido en el bashrc.
#manda un correo al admin con la hora indicando que se ha producido un acceso 

use Email::Send::SMTP::Gmail;


my $correo = "pecera.correo@gmail.com";
my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'pecera.correo@gmail.com',
                                                 -pass=>'wfsnglhnqfjcvmhw');
my $hora = localtime();
my $mensaje = "se ha producido un login como root: $hora";
print "session error: $error" unless ($mail!=-1);
$mail->send(-to=> 'guillermovclase@gmail.com', -subject=>'Login', -body=>$mensaje, -attachments=>'full_path_to_file');
$mail->bye;