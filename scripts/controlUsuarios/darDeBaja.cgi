#!/usr/bin/perl 

use strict; #me da problemas con la palabra true y no puedo insertar booleanos en mysql
use warnings;

use CGI; #para poder incovarlo desde la pagina web
use Linux::usermod; #para crear el usuario
use CGI::Session;
use DBI; #para conectar con la base de datos.
use Time::Piece::MySQL;
#use Email::Address; #para parsear el correo


my $username;
my $q = CGI->new;
#print $q->header();
my $session = new CGI::Session;
$session->load();
my @autenticar = $session->param;

if(@autenticar eq 0){
    $session->delete();
    $session->flush();
    print $q->redirect("/index.html");
}elsif($session->is_expired){
    $session->delete();
    $session->flush();
    print $q->redirect("/index.html");
}else{
    print $q->header;
    $username = $session->param("username");
	print qq(
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/estilos/styles.css" type="text/css">
        <link rel="stylesheet" href="https://unpkg.com/purecss@2.1.0/build/pure-min.css" integrity="sha384-yHIFVG6ClnONEA5yB5DJXfW2/KC173DIQrYoZMEtBvGzmf0PKiGyNEqe9N6BNDBH" crossorigin="anonymous">
    <title>Pecera Dev</title>
</head>
<body>
    <div class="navbar">
        <a href="/cgi-bin/verificarLogin.cgi">Home</a>
        <a href="/cgi-bin/verificarLogin.cgi">Login</a>
        <a class="/signUp.html">Sign up</a>
        <a href="/cgi-bin/monitor.cgi">Servicios</a>
    </div>

        <div class="cabecera">
            <h1>Borrar usuario</h1>
        </div>

        <form class="pure-form" method="POST" action="/cgi-bin/borrarUsr.cgi">
        	<h2>Confirma tus credenciales para borrar tu usuario</h2>
            <fieldset>
                <input  name="username" placeholder="login" />
                <input type="password" name="password" placeholder="Password" />
                <button type="submit" class="pure-button pure-button-primary">Sign in</button>
            </fieldset>
        </form>
);
}
