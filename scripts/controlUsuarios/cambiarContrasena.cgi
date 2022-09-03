#!/usr/bin/perl

use strict;
use warnings;

use CGI;
use CGI::Session;
use Linux::usermod;
use Authen::PAM;

my $username; #toma el parametro username del formulario
my $password; #toma el parametro password del formulario
my $q = CGI->new;
#print $q->header();
my $session = new CGI::Session;
$session->load();
my @autenticar = $session->param;


#primero verificamos la sesion.
if(@autenticar eq 0){
    $session->delete();
    $session->flush();
    print $q->redirect("/index.html");
}elsif($session->is_expired){
    $session->delete();
    $session->flush();
}else{
    #print $q->header;
    $username = $q->param("usuario");
    $password = $q->param("password");
    my $n_password = $q->param("n_password");
    my $nc_password = $q->param("nc_password");
    my $service = "passwd";
    my $pamh;

    sub my_conv_func {
        my @res;
        while ( @_ ) {
            my $code = shift;
            my $msg = shift;
            my $ans = '';

            $ans = $username if ($code == PAM_PROMPT_ECHO_ON());
            $ans = $password if ($code == PAM_PROMPT_ECHO_OFF());
     
           push @res, (PAM_SUCCESS(),$ans);
        }
        push @res, PAM_SUCCESS();
        return @res;
    }

    if (!ref($pamh = new Authen::PAM($service, $username, \&my_conv_func))) {
        print "Authen::PAM fallo al iniciar\n";
        exit 1;
        #redireccion.
    }

    my $res = $pamh->pam_authenticate;

    if($res == PAM_SUCCESS()){
        my $usr = Linux::usermod->new($username);
        if($n_password ne $nc_password){
            #redirigir a error.
            print $q->redirect("/cambiarContrasenaError.html");
        }else{
            $usr->set('password',$n_password);
            print $q->redirect('/index.html');
        }
    }else{
        print $q->redirect('/loginError.html');
    }
}
