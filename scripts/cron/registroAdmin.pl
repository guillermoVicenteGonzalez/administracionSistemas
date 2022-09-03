#!/usr/bin/perl

#este script genera un informe que enviara al admin todas las noches.
#para ello hay que programar un cron job

use DBI;
use Filesys::DiskUsage qw/du/;
use Proc::ProcessTable;
use Email::Send::SMTP::Gmail;

my $memoria = "/var/pecera/datos/free.txt";
my $comandos = "/var/pecera/datos/comandos.txt";
my $file = "/tmp/informe.txt";
open(my $fp, '>', $file) or die "Error al abrir el archivo $file";
print $fp "\n---------------------\n# programas mas usados #\n---------------------\n\n";
open(FH, '<', $comandos) or die $!;
my @arr;

   print $fp "comando:\tporcentaje\n";
while(<FH>){
   @arr=split /\s+/,$_;
   print $fp "$arr[9]:\t\t$arr[2]\n";
}
close(FH);
print $fp "\n---------------------\n# Uso de memoria #\n---------------------\n\n";
open(FH, '<',$memoria) or die $!;
while(<FH>){
	print $fp "$_"
}

print $fp "\n---------------------\n# Uso de disco #\n---------------------\n\n";

my $dbh = DBI->connect('DBI:MariaDB:database=global;host=localhost',
                       'gestor','Yg0yubme7jyHzCOf',
                       { RaiseError => 1, PrintError => 0,AutoCommit => 1 });

my $sth = $dbh->prepare("SELECT Nombre FROM usuarios");
$sth->execute();

my @usuarios;
while (@usuarios = $sth->fetchrow_array){
    my $usuario = $usuarios[0];
    print $fp "Nombre del usuario: ";
    printf $fp "$usuario\n";
    my $dir = "/home/" . $usuario . "/";
    my $tam = du ( { 'human-readable' => 1 } , $dir );
    printf $fp '%-20s %-20s' . "\n","Espacio usado","Directorio";
    printf $fp '%-20s %-20s' . "\n","$tam","$dir";
}
close($fp);
close(FH);
my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'pecera.correo@gmail.com',
                                                 -pass=>'wfsnglhnqfjcvmhw');
my $tiempo = localtime();
my $mensaje = "generado en: $tiempo\nreporte del sistema adjunto.";
$mail->send(-to=> 'guillermovclase@gmail.com', -subject=>'Reporte del sistema', -body=>$mensaje, -attachments=>$file);
$mail->bye;

