#!/usr/bin/perl

#este script verifica si existen sesiones abiertas.
#si existe una sesion abierta redirige al panel del usuario de la sesion
#si  la sesion ha expirado redirige a una pantalla de error
#si la sesion no existe redirige a login

use strict;
use warnings;
use CGI;
use CGI::Session;

my $q = CGI->new;
my $session = new CGI::Session;
$session->load();
my @autenticar = $session->param;

if(@autenticar eq 0){
    $session->delete();
    $session->flush();
    print $q->redirect("/loginScreen.html");
}elsif($session->is_expired){
    $session->delete();
    $session->flush();
    #redirigir a "tu sesion ha expirado"
    print $q->redirect("/errorGeneral.html");
}else{
    print $q->redirect("landing.cgi");
}