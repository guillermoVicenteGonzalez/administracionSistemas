#!/usr/bin/perl

#este script genera el menu del usuario.
#primero verifica que esté autentificado con su sesion.

#esto va en todos los script
use strict;
use warnings;

use CGI;
use CGI::Session;
use Linux::usermod;

my $username;
my $q = CGI->new;
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
    print $q->redirect("/errorGeneral.html")
}else{
    print $q->header;
    $username = $session->param("username");
    print qq(<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/purecss@2.1.0/build/pure-min.css" integrity="sha384-yHIFVG6ClnONEA5yB5DJXfW2/KC173DIQrYoZMEtBvGzmf0PKiGyNEqe9N6BNDBH" crossorigin="anonymous">
    <link rel="stylesheet" href="/estilos/styles.css">

    <title>Pecera</title>
</head>
<style>

</style>
<body>
    <div class="navbar">
        <a href="/index.html">Home</a>
        <a class="active" href="/loginScreen.html">Login</a>
        <a href="/signUp.html">Sign up</a>
        <a href="/cgi-bin/monitor.cgi">Servicios</a>
        <a href="cerrarSesion.cgi">cerrarSesion</a>
    </div>

        <div class="cabecera">
            <h1>Panel de usuario $username</h1>
        </div>

        <div class="grid-container">
            <a class="tarjeta" href="/modificar.html"> Modificar datos</a>
            <a class="tarjeta" href="/cambiarContrasena.html">cambiar contraseña</a>
            <a class="tarjeta" href="/darDeBaja.html ">dar de baja</a>
            <a class="tarjeta" href="/wordpress/wp-signup.php">Solicitar web</a>
            <a class="tarjeta" href="/squirrelmail">Correo</a>
            <a class="tarjeta" href="/apuntes">apuntes</a>
        </div>

        
        <div class="footer">
            <p>© PeceraDev - 2022 | Jorge Prieto y Guillermo Vicente</p>
        </div>


</body>
</html>

);

}
