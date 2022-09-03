#!/usr/bin/perl

#este script esta asociado a un cronjob.
#sirve para gestionar la posibilidad de un usuario que no terminase el registro
#comprueba con una consulta todos los usuarios que no han terminado de registrarse.
#estos usuarios tienen el campo registrado a 0 y aun tienen codigo
#se borra a estos usuarios y usando su nombre se borran de /etc/passwd

use Linux::usermod; #para crear el usuario
use File::Path qw(make_path remove_tree); #para crear el directorio
use DBI; #para conectar con la base de datos.
use Time::Piece::MySQL;
use Date::Parse;

my $id;
my $nombre;
my $diff;
my $tiempoLocal = localtime;
my $fecha;
my $hora;
my @arr;
my $dbh;
my @borrarUsrs; #array con los id de los usuarios a borrar.

$tiempoLocal = $tiempoLocal->mysql_datetime;
my @arrLocal = split(' ',$tiempoLocal);
my $fechaLocal = $arrLocal[0];
my $horaLocal = $arrLocal[1];

print "fechaLocal: $fechaLocal, hora local: $horaLocal";
print "\n";

$dbh = DBI->connect('DBI:MariaDB:database=global;host=localhost',
                       'gestor','Yg0yubme7jyHzCOf',
                       { RaiseError => 1, PrintError => 0 });
$sth = $dbh->prepare("select nombre, h_registro, id from usuarios where registrado=0") or die;
$sth->execute();



while(@row = $sth->fetchrow_array){
	$nombre = $row[0];
	$id = $row[2];
	if(!$row[1]){
		#error
		print "entro en error\n";
	}else{
		@arr = split(' ',$row[1]);
		$fecha = $arr[0];
		$hora = $arr[1];

		$diff = str2time($hora) - str2time($horaLocal);

		if($diff > 3600){
			#ha pasado una hora. Borramos el usuario y su BD
			Linux::usermod->del($nombre);
			#si hago esto aqui me joroba la otra consulta y la necesito para
			#$sth = $dbh->prepare("delete from usuarios where id=?");
			#$sth->execute($id);
			push(@borrarUsrs, $id);
		}
	}
}

foreach my $i (@borrarUsrs){
	$sth = $dbh->prepare("delete from usuarios where id=?");
	$sth->execute($i);
}

$dbh->disconnect;