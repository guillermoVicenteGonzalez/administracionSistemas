#!/usr/bin/perl

#este script gestiona el login de los usuarios.
#previamente verificarLogin verifica si hay sesiones abiertas.
#Si no existe una sesion abierta redirige a esta pantalla

#esto va en todos los script
use strict;
use warnings;

use CGI;
use CGI::Session;
use Linux::usermod;
use Authen::PAM;
use POSIX qw(ttyname);

my $q = CGI->new;
#print $q->header();

my $username = $q->param(-name => 'username',-value => $q->param('username'));
my $password = $q->param(-name => 'password',-value => $q->param('password'));


my $service = "passwd";
my $pamh;
my $session;


sub my_conv_func {
    my @res;
    while ( @_ ) {
        my $code = shift;
        my $msg = shift;
 		my $ans = '';

 		$ans = $username if ($code == PAM_PROMPT_ECHO_ON());
 		$ans = $password if ($code == PAM_PROMPT_ECHO_OFF());
 
       push @res, (PAM_SUCCESS(),$ans);
    }
    push @res, PAM_SUCCESS();
    return @res;
}

if (!ref($pamh = new Authen::PAM($service, $username, \&my_conv_func))) {
    print "Authen::PAM fallo al iniciar\n";
    exit 1;
    print $q->redirect("/errorGeneral.html");
}

my $res = $pamh->pam_authenticate;

if($res == PAM_SUCCESS()){
    $session = CGI::Session->new();
    $session->save_param($q);
    $session->expires("+1h");
    $session->flush();
    print $session->header(-location => "landing.cgi");
	#print $q->redirect('/index.html');
}else{
	print $q->redirect('/loginError.html');
}
