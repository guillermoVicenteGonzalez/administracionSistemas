#!/usr/bin/perl 

#este script lee el codigo introducido y verifica que exista en la BD 

use strict; 
use warnings;

use Quota;
use CGI; #para poder incovarlo desde la pagina web
use Linux::usermod; #para crear el usuario
use File::Path qw(make_path remove_tree); #para crear el directorio
use File::chown; #las opciones por defecto de Path no me cambian bien el dueño del directorio
use DBI; #para conectar con la base de datos.
use Email::Send::SMTP::Gmail;
#use Email::Address; #para parsear el correo


#para que funcione el cgi
my $q = CGI->new;
my @row;

#parametros de usuario.
my $sth;
my $codigo = $q->param('codigo');
my $user; #para pillar el objeto user de usermod
#para usar los datos del usuario en caso de fallo.
my %hashUsuario = $q->cookie('COOKIE_USUARIO');
my $nombre = $hashUsuario{'nombre'};
my $correo = $hashUsuario{'correo'};
my $direccion = $hashUsuario{'direccion'};


#print $q->header();



#conecto con la base de datos global con el usuario gestor cuya contraseña esta vacía.
my $dbh = DBI->connect('DBI:MariaDB:database=global;host=localhost',
                       'gestor','Yg0yubme7jyHzCOf',
                       { RaiseError => 1, PrintError => 0,AutoCommit => 1 });

#busco en la base de datos al usuario con el codigo que se ha introducido.
#Si ningun codigo coincide, entonces error
$sth = $dbh->prepare("SELECT codigo FROM usuarios WHERE codigo=?");
$sth->execute($codigo);

my ($count) = $sth->fetchrow_array();

if(!$count){
    #error, no he encontrado el codigo en la base de datos
    #primero verifico si hay usuario que se corresponda al de la cookie que no este registrado
    #primero de todo verifico que la cookie no este vacia
    if(!$nombre){
        print "la cookie esta vacia";
    }else{
        #si la cookie no esta vacia hago un select con ella
        $sth = $dbh->prepare("SELECT registrado FROM usuarios WHERE nombre=?");
        $sth->execute($nombre);
        ($count) = $sth->fetchrow_array();
        if($count eq 1){
            #el usuario ya existe y esta registrado. No lo borro
            #print "usuario ya registrado";
            #lo dejo en blanco porque esta situacion en realidad no tiene sentido
        }elsif($count eq 0){
            #el usuario existe y no esta registrado. Los codigos no coinciden
            #por simplicidad haremos que se borre su info de la bd y de passwd
            #como no está registrado no se ha creado su /home
            $sth = $dbh->prepare("delete from usuarios where nombre=?");
            $sth->execute($nombre);
            $dbh->disconnect;
            Linux::usermod->del($nombre);
        }
    }
print $q->redirect('/codigoError.html');

}else{
    $sth = $dbh->prepare("SELECT nombre FROM usuarios WHERE codigo=?");
    $sth->execute($codigo);
    ($count) = $sth->fetchrow_array();
    #con el nombre cogemos el hash de usermod y asi le quitamos el nologin
    $user = Linux::usermod->new($count);
    $user->set('shell','/bin/bash');
    #print "las cuotas se han instalado correctamente";

    #tambien hay que actualizar la base de datos.
    $sth = $dbh->prepare("update usuarios set codigo=0,registrado=1 where codigo=? and nombre=?");
    $sth->execute($codigo, $count);
    $dbh->disconnect;
    print $q->redirect('/index.html');
    #exit 1;
}
#print "$count";
# si count es null -> error
# si count no es null
# => modifico la entrada con usermod para poner /bin/bash
# => modifico la entrada de la base de datos para cambiar el campo registrado y codigo a 0
#print $q->redirect('https://www.tutorialspoint.com/perl/perl_hashes.htm');

