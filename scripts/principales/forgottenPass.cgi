#!/usr/bin/perl

#en caso de contraseña olvidada se reemplaza la antigua por un codigo de 8 digitos.
#el codigo se envia al email asociado al usuario que lo ha solicitado.
#el email se obtiene haciendo una consulta a la base de datos
#se podria mejorar usando cookies

#esto va en todos los script
use strict;
use warnings;

use CGI;
use DBI;
use Linux::usermod;
use Email::Send::SMTP::Gmail;

my $q = CGI->new;
#print $q->header();

my $username = $q->param("usuario");
my $codigo = int(rand( 99999999-10000000+1 ) ) + 10000000;
my $sth;
my $user = Linux::usermod->new($username);
my $uid = $user->get('uid');
my $dbh = DBI->connect('DBI:MariaDB:database=global;host=localhost',
                       'gestor','Yg0yubme7jyHzCOf',
                       { RaiseError => 1, PrintError => 0 });
$sth = $dbh->prepare("select email from usuarios where uid=?") or die;
$sth->execute($uid);
my $correo = $sth->fetchrow_array;

my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'pecera.correo@gmail.com',
                                                 -pass=>'wfsnglhnqfjcvmhw');

print "session error: $error" unless ($mail!=-1);
if($mail == -1){
    #error mandando el correo
    #redirigir a ha habido un error.
    print $q->redirect("/errorGeneral.html");
}else{
    my $mensaje = 'tu nueva contraseña es ${codigo}, para cambiar la contraseña logeate y selecciona la opcion cambiar contraseña';
    $mail->send(-to=> $correo, -subject=>'Recuperar contraseña', -body=> $codigo, -attachments=>'full_path_to_file');
    $mail->bye;
    $user->set("password",$codigo);
    #print $q->redirect('/correo.html');
    #aqui podriamos directamente usar el PAM para logearlo, pero mejor ser sencillo
    print $q->redirect('/cgi-bin/verificarLogin.cgi');
}
