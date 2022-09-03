#!/usr/bin/perl 


=pod
*******************************************************
*Cosas por hacer:
*	chown a las carpetas creadas
*	redireccionar a las paginas que tocan (faltan los htmls)
*	End of script output before headers
*	tratamiento de errores: si crea un usuario pero falla la DB existe un usuario fuera de la DB.
*	verificar que no hay campos vacios (+ mensaje error)
*******************************************************
=cut
#

use strict; #me da problemas con la palabra true y no puedo insertar booleanos en mysql
use warnings;

use CGI; #para poder incovarlo desde la pagina web
use Linux::usermod; #para crear el usuario
use File::Path qw(make_path remove_tree); #para crear el directorio
use File::chown; #las opciones por defecto de Path no me cambian bien el dueño del directorio
use DBI; #para conectar con la base de datos.
use Email::Send::SMTP::Gmail;
use Time::Piece::MySQL;
#use Email::Address; #para parsear el correo


#para que funcione el cgi
my $q = CGI->new;

#parametros de usuario
my $nombre  = $q->param('usuario');
my $contrasena   = $q->param('password');
my $esProfesor = $q->param('esProfesor');
my $correo = $q->param('email');
my $direccion = $q->param('direccion');
my $grupo; #alumno o profesor
my $nombreUsr = $q->param('nombre');
my $ape1 = $q->param('apellido1');
my $ape2 = $q->param('apellido2');
my $nombreCompleto = "$nombreUsr $ape1 $ape2";
my $ruta; #ubicacion del directorio del usuario
my $directorio; #directorio del usuario para hacer con make_path
my $codigo = int(rand( 9999-1000+1 ) ) + 1000;
my %datosUsuario; #hash que le pasamos a la cookie
my $cookie; #cookie para funcionalidad extra
#conseguimos un hash de los usuarios para verificar.
my %usuarios = Linux::usermod->users();
my $sth; #para la base de datos
my $fecha = localtime;
$fecha = $fecha->mysql_datetime;
my $uid; #uid para insertar en la BD


#compruebo que no haya cadenas vacias y en caso afirmativo redirijo a pagina de error.
if(!$nombre | !$contrasena | !$correo | !$ direccion){
	#redireccionar a una pagina de error
	print $q->redirect('/signUpErrorFields.html');
	exit 0;
}

#compruebo que no esté intentando logearse como root admin u otros usuarios "peligrosos"
#logearse como el admin podria redireccionar a una pantalla de administracion
if($nombre eq "root" or $nombre eq "admin" or $nombre eq '::' or $nombre eq 'ssh'){
	#redireccionar a una pagina de error
	print $q->redirect('/signUpErrorRoot.html');
	exit 0;
}

#conecto con la base de datos global con el usuario gestor cuya contraseña esta vacía.
my $dbh = DBI->connect('DBI:MariaDB:database=global;host=localhost',
                       'gestor','Yg0yubme7jyHzCOf',
                       { RaiseError => 1, PrintError => 0 });


#esto estaria guay automatizarlo pero de momento funciona
if($esProfesor){
	$grupo = '1003';
}else{
	$grupo = '1002';
}

#para la cookie
%datosUsuario = (
	-nombre => $nombre,
	-correo => $correo,
	-direccion => $direccion,
);

#verifico que el usuario no exista en /etc/passwd
for(keys %usuarios){
	if($_ eq $nombre){
		#el usuario ya existe asi que mando error
		print $q->redirect('/signUpErrorExists.html');
		exit 0;
	}
}

#la ruta se crea posteriormente con ldap, pero se la especifico ya.
$ruta = "/home/$nombre"; 
Linux::usermod->add($nombre,$contrasena,"",$grupo,$nombreCompleto ,$ruta,"nologin");
my $usr = Linux::usermod->new($nombre);
$uid = $usr->get('uid');


#inserto los datos en la BD
$sth = $dbh->prepare("insert into usuarios (nombre, nombreUsr, ape2, ape1, isProfesor, email, direccion, codigo, registrado, h_registro, uid) values (?,?,?,?,?,?,?,?,?,?,?)") or die;
if($esProfesor){
	$sth->execute($nombre, $nombreUsr, $ape2, $ape1, 1, $correo, $direccion, $codigo, 0, $fecha, $uid) or die;
}else{
	$sth->execute($nombre, $nombreUsr, $ape2, $ape1, 0, $correo, $direccion, $codigo, 0, $fecha, $uid) or die;
}


#no funciona la parte del chown. Hay que usar ldap o suexec
=pod
$directorio = make_path($ruta,{
	chmod => 0755,
	owner => $nombre,
	group => $grupo,
});
=cut

#gestiono el envio del correo electronico
my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'pecera.correo@gmail.com',
                                                 -pass=>'wfsnglhnqfjcvmhw');

print "session error: $error" unless ($mail!=-1);
if($mail == -1){
	#error mandando el correo
	Linux::usermod->del($nombre); #borro el usario 
	$sth = $dbh->prepare("delete from usuarios where nombre=?");
	$sth->execute($nombre);#borro la entrada de la base de datos
	$dbh->disconnect;
	$cookie = $q->cookie(-name=> 'COOKIE_USUARIO',
					-value=> 'vacio',
					-expires=>'+1h',
					-path=>'/');
	print $q->redirect(-uri => '/index.html', -cookie => $cookie);

	#redirigir a ha habido un error.
}else{
	my $mensaje = "tu codigo es $codigo";
	$mail->send(-to=> $correo, -subject=>'Registro', -body=>$mensaje, -attachments=>'full_path_to_file');
	$mail->bye;
	#print $q->redirect('/correo.html');
	%datosUsuario =  (nombre => $nombre,
					correo => $correo,
					direccion => $direccion,
					);


	$cookie = $q->cookie(-name=> 'COOKIE_USUARIO',
					-value=> \%datosUsuario,
					-expires=>'+1h',
					-path=>'/');

	print $q->redirect(-uri => '/correo.html', -cookie => $cookie);
}




