#!/usr/bin/perl

#la idea era usar ldap pero me da problemas. Este script no se usa
#en su lugar se usa crearCuotas2.pl

use Quota;
use Net::LDAP;



my $usuario = %ENV{'PAM_USER'};

#base de datos de ldap
my $ldap = Net::LDAP->new('localhost') or die "error servidor";
#aqui puede haber error
$ldap->bind('cn=admin,dc=pecera,dc=local',password => "2105");

my $search = $ldap->search(base=>"ou=People,cd=pecera,dc=local",filter => "(uid=$usuario)");
if($search->error ne "Success"){
	die $search->error."no existe usuario con esas credenciales";
}elsif((scalar $search->entries) > 1){
	die "hay mas de un elemento coincidente";
}else{
	my $uid;
	foreach $entry($search->entries){
		$uid = $entry->get_value('uidNumber');
	}
	my $hlimit = 83886080;
	my $slimit = 62914560;
	my $dev = Quota::getqcarg('/');
	if((scalar $uid) ge 5000){
		Quota::setqlim($dev,$uid,$slimit,$hlimit,0,0,0,0);
		print "las cuotas se han instalado correctamente"
	}

}