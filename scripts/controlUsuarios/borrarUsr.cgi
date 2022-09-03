#!/usr/bin/perl 

use strict; #me da problemas con la palabra true y no puedo insertar booleanos en mysql
use warnings;

use CGI; #para poder incovarlo desde la pagina web
use Linux::usermod; #para crear el usuario
use CGI::Session;
use File::Path qw(make_path remove_tree); #para crear el directorio
use DBI; #para conectar con la base de datos.
use Authen::PAM;
use File::Find qw(finddepth);
#use Email::Address; #para parsear el correo


my $username;
my $q = CGI->new;
#print $q->header();
my $session = new CGI::Session;
$session->load();
my @autenticar = $session->param;
my $nombreUsr = $q->param('username');
my $password = $q->param('password');


if(@autenticar eq 0){
    $session->delete();
    $session->flush();
    print $q->redirect("/index.html");
}elsif($session->is_expired){
    $session->delete();
    $session->flush();
    print $q->redirect("/index.html");
}else{
    $username = $session->param("username");
    my $service = "passwd";
    #my $password = $q->param('password');;
    my $pamh;
    my $session;


    sub my_conv_func {
        my @res;
        while ( @_ ) {
            my $code = shift;
            my $msg = shift;
            my $ans = '';

            $ans = $nombreUsr if ($code == PAM_PROMPT_ECHO_ON());
            $ans = $password if ($code == PAM_PROMPT_ECHO_OFF());
     
           push @res, (PAM_SUCCESS(),$ans);
        }
        push @res, PAM_SUCCESS();
        return @res;
    }

    if (!ref($pamh = new Authen::PAM($service, $nombreUsr, \&my_conv_func))) {
        print "Authen::PAM fallo al iniciar\n";
        exit 1;
        #redireccion.
    }

    my $res = $pamh->pam_authenticate;

    if($res == PAM_SUCCESS()){
        if($nombreUsr eq $username){
            Linux::usermod->del($nombreUsr);
            my $dbh = DBI->connect('DBI:MariaDB:database=global;host=localhost',
                       'gestor','Yg0yubme7jyHzCOf',
                       { RaiseError => 1, PrintError => 0 });
            my $sth = $dbh->prepare("delete from usuarios where nombre=?");
            $sth->execute($nombreUsr);
            print $q->redirect('/index.html');
            #borrar directorio
        }else{
            #print $q->redirect('/loginError.html');
            print $q->redirect("/errorGeneral.html")
        }
    }else{
        #print $q->redirect('/loginError.html');
        print $q->redirect("/errorGeneral.html")
    }	
}
    $session->delete();
    $session->flush();