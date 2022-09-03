#!/usr/bin/perl

#este script lee los ficheros generados por monitorservicios.sh
#en funcion de la lectura de los archivos imprime divs de una clase u otra

use CGI;
use File::Slurp;

my $q = CGI->new;

my $apache = read_file('/var/www/html/estado/apache2');
my $sshd = read_file('/var/www/html/estado/sshd');
my $dovecot = read_file('/var/www/html/estado/dovecot');
my $postfix = read_file('/var/www/html/estado/postfix');
my $mariadb = read_file('/var/www/html/estado/mariadb');
my $quotaon = read_file('/var/www/html/estado/quotaon');

my @servicios = ($apache, $sshd, $dovecot, $postfix, $mariadb, $quotaon);
my @nombresServicios = ("Web", "SSH", "SMTP", "IMAP", "BASE DE DATOS", "CUOTAS");
my $i = 6;

print $q->header;


print qq(
  <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/purecss@2.1.0/build/pure-min.css" integrity="sha384-yHIFVG6ClnONEA5yB5DJXfW2/KC173DIQrYoZMEtBvGzmf0PKiGyNEqe9N6BNDBH" crossorigin="anonymous" type="text/css">
    <link href="{{ .Site.BaseURL }}css/css.css" rel="stylesheet">
    <link rel="stylesheet" href="/estilos/styles.css">
    <link rel="stylesheet" href="/estilos/monitor.css"
</head>
<body>
    <div class="navbar">
        <a href="/index.html">Home</a>
        <a href="/cgi-bin/verificarLogin.cgi">Login</a>
        <a href="/signUp.html">Login</a>
        <a class="active">Servicios</a>
    </div>

        <div class="cabecera">
            <h1>Estados</h1>
        </div>
        <div class="cajas">
        );

        for ($i = 0; $i < @servicios; $i++){
          my $servicio = $nombresServicios[$i];
          if($servicios[$i] != 1){
            print qq(
              <div class="caja_inactivo">
                <h3>$servicio</h3>
                <label class="servicio_inactivo">Inactivo</label>
              </div>);
          }else{
            print qq(
              <div class="caja_activo">
                <h3>$servicio</h3>
                <label class="servicio_activo">Activo</label>
              </div>);
          }
        }
print qq(
        </div>
</body>
</html>);
