#!/usr/bin/perl

#este script cierra le asesion.
#tras cerrar la sesion, al encontrarnos en cgi-bin, redirije a index.html

#esto va en todos los script
use strict;
use warnings;

use CGI;
use CGI::Session;

my $q = CGI->new;
my $session = new CGI::Session;
$session->load();
$session->delete();
$session->flush();

print $q->redirect("../index.html");