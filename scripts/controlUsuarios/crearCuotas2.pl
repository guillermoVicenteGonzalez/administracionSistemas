#!/usr/bin/perl

#version mas cutre que la original pero que funciona
#verifica en la BD que usuarios no tienen cuota asignada y se la asigna.
#este script esta metido en el archivo de configuracion de ldap.
#cada vez que un usuario hace login se ejecuta y actualiza las cuotas de todo el mundo ("que no tuviera cuotas claro")
#seria mas comodo hacer esto en el script de registro pero no funciona por algun motivo
#supongo que sera porque hay cosas aun no configuradas cuando se ejecuta ese script

use DBI;
use Quota;
use Linux::usermod;

my $hlimit = 83886080;
my $slimit = 62914560;
my $dev = Quota::getqcarg('/');
my $user;
my $nombre;
my $uid;
my @usuarios;
#inicio sesion en la base de datos
my $dbh = DBI->connect('DBI:MariaDB:database=global;host=localhost',
                       'gestor','Yg0yubme7jyHzCOf',
                       { RaiseError => 1, PrintError => 0 });
$sth = $dbh->prepare("select uid, nombre from usuarios where quota=0") or die;
$sth->execute();


while(@row = $sth->fetchrow_array){
	$uid = $row[0];
	$nombre = $row[1];
	if($uid){
		Quota::setqlim($dev,$uid,$slimit,$hlimit,0,0,0,0);
		print "las cuotas se han instalado correctamente para $nombre\n";
		push(@usuarios,$uid);
	}
}

foreach my $i (@usuarios){
	$sth = $dbh->prepare("update usuarios set quota=1 where uid=?") or die;
	$sth->execute($i);
}
$dbh->disconnect;