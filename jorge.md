## Sesion 11

primero hay que instalar apache.

hay que activar un modulo usando

a2enmod cgi

cgi viene de common g interface

```bash
a2enmod cgi
```

los scripts que queramos ejecutar desde la pagina tienen que estar en otro directorio. Concretamente /usr/lib/cgi-bin

creamos un scriptque se llame holamundo.cgi

Las extensiones en linux no valen menos en este caso. Los scripts a ejecutar tienen que tener extension cgi

La estructura tiene que ser especial tambien.

- la primera linea es un comentario con # con la ruta del programa que lo va a ejecutar (perl)
  
- A partir de ahi cualquier codigo perl deberia funcionar
  
- Las librerias con use debajo del comentario
  

```perl
#/usr/bin/perl

print "Hola mundo";
```

Para ejecutar los cgi hay que poner la ip/cgi-bin

Va a dar un error, eso es porque faltan aun tres cosas por hacer.

Truco: siempre que hagamos un script cgi

Los scripts para que se puedan lanazar no pueden ser del root. Eso es por una directiva de seguridad de apache.

Hay por tanto que cambiar el propietario del script. Normalmente al dueño del servidor

```bash
chown www-......
```

Aun dara otro error.

El programa tiene que tener permisos de ejecucion., chmod a+x

Sigue sin funcionar, falta una tercera cosa por hacer.

Cuando un navegador printea informacion. hay que enviar una cabecera al navegador.

Ese print (cabecera) es: nos lo dice luego.

Como hago "scans", como tomo el input del usuario.

Hay que hacer formularios html. Se espera que utilicemos templates. Pure css no esta mal para darle caña y evita mierdas como validaciones etc. Definitivamente mola y nos va a ahorrar tiempo.

Una vez tenemos nuestra template con nuestros campos y toda la pesca tneemos que coger los datos de las cajas y meterlas en una variable perl. Esto SIEMPRE tiene que ser con formularios html.

Hay un atributo del campo form que se llama action. Action solo permite llevar los datos a una pagina web entonces tenemos que decirle a action que lleve los datos a un cgi. Hay que especificar la ruta completa en plan

```html
<form action = "/cgi-bin/login.cgi"> </form>
```

hay que darle name a las etiquetas.

```html
<input name="email" type="email"> </input>
```

La contraseña se ve en la ip. Hay que ocultarla. Hay dos formas, la por defecto es usando el metodo get que no la oculta. La segunda que si

hay que poner method="POST" en la etiqueta form

Hay un modulo en metacepan que se llama cgi. Es de lee jhonson.

Se pueden hcaer mil cosas pero nosotros necesitamos 3 lineas que son

```perl
#!/usr/bin/perl


#esto va siempre 
use CGI
my $q = CGI->new;  #esto en teoria es lo de la cabecera que nos decia luego.

print $q ->header(); # esto es necesario para poder hacer prints

#para tomar campos usamos la linea 
#my value q param
#o algo asi
#es importante usar el atributo name en lugar de param_name
```

Estos scripts conviene probarlos antes con el interprete de perl para no desesperarse usandolos en la web.

Recuerda que la direccion de los scripts para ponerla en el navegador es

ip/cgi-bin/nombreScript.cgi

el q header es necesario para todos los scripts menos cuando se quiera redireccionar a un usuario en una pagina web, por ejemplo en el login. Si el usuario mete la contraseña bien hay que redireccionarle a otra

El codigo para mandar a otra pagina es redirect (buscar lo demas en el manual).

Para redireccionar a mis propias paginas copio la ruta a lo burro aunque sospecho que la ip como puede cambiar tendre que parametrizarlo.

## Para sobraos

Si nos logeamos en la aplicacion el roundcube nos va a pedir otra vez la contraseña. Para evitar esto podemos usar el autologin del roundcube (es cambiar una linea de codigo).

con buscar roundcube autologin sirve

hay que pasarle unos parametros especificos en el href del roundcube para que funcione el autologin.

openldap (alternativa a usermod) es mas potente pero igual da mas por culo. Primero probamos con usermod y luego si sobre tiempo usamos esto.

Montar servidor dns (Bind9) para acceder a la pagina pero por nombre y no con ip.

## gilipolleces

lynx: navegador para modo terminal

gp: lo instalamos con apt. Sirve para usar el raton en modo terminal.
