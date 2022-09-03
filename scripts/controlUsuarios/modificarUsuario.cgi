#!/usr/bin/perl

#esto va en todos los script
use strict;
use warnings;

use CGI;
use CGI::Session;
use Linux::usermod;
use Authen::PAM;
use POSIX qw(ttyname);
use DBI;

my $q = CGI->new;

my $nombreUsr = $q->param("nombre");
my $ape1 = $q->param("apellido1");
my $ape2 = $q->param("apellido2");
my $correo = $q->param("email");
my $direccion = $q->param("direccion");
my $isProfesor = $q->param("esProfesor");

my $username;

#print $q->header();
my $session = new CGI::Session;
$session->load();
my @autenticar = $session->param;
my $login = $q->param('usuario');
my $password = $q->param('password');
my $sth;

#primero autentico la sesion.
if(@autenticar eq 0){
    $session->delete();
    $session->flush();
    print $q->redirect("/index.html");
}elsif($session->is_expired){
    $session->delete();
    $session->flush();
    print $q->redirect("/index.html");
}else{
    #primero verifico que no haya campos vacios.

    #ahora autentico con PAM las credenciales introducidas.
    my $service = "passwd";
    my $pamh;
    sub my_conv_func {
        my @res;
        while ( @_ ) {
            my $code = shift;
            my $msg = shift;
            my $ans = '';

            $ans = $login if ($code == PAM_PROMPT_ECHO_ON());
            $ans = $password if ($code == PAM_PROMPT_ECHO_OFF());
     
           push @res, (PAM_SUCCESS(),$ans);
        }
            push @res, PAM_SUCCESS();
            return @res;
    }

    if (!ref($pamh = new Authen::PAM($service, $login, \&my_conv_func))) {
        print "Authen::PAM fallo al iniciar\n";
        exit 1;
        $q->redirect("https://google.es");#redireccion.
    }

    my $res = $pamh->pam_authenticate;

    if($res == PAM_SUCCESS()){
        #ahora uso usermod y dbi para modificar la informacion pertinente
        #falta cambiar el grupo con el usermod
        #tambien hay que procesar el esprofesor de los cojones
        my $usr = Linux::usermod->new($login);
        my $uid = $usr->get('uid');
        my $dbh = DBI->connect('DBI:MariaDB:database=global;host=localhost',
                       'gestor','Yg0yubme7jyHzCOf',
                       { RaiseError => 1, PrintError => 0 });
        $sth = $dbh->prepare("update usuarios set nombreUsr = ?, ape2= ?, ape1 = ?, email = ?, direccion = ? where uid=?");
        $sth->execute($nombreUsr,$ape2,$ape1, $correo, $direccion, $uid);
        print $q->redirect('/index.html');
        #redireccion: informacion cambiada con exito.
    }else{
      #error.
        print $q->redirect('/loginError.html');   
    }

}
