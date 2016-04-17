#!/bin/sh
__WSGI_PATH="$(pwd)/atmospi.wsgi"
__ATMOSPI_DIR="$(pwd)"
__ATMOSPI_MODULE_DIR="$__ATMOSPI_DIR/Atmospi"
rm 000-atmospi.conf >& /dev/null
cat << EOF > 000-atmospi.conf
<VirtualHost *:80>
    ServerName atmospi
    ServerAlias atmospi1 atmospi2 atmospi3 atmospi4 atmospi5 atmospi6 atmospi7 atmospi8 atmospi9 atmospi10

    WSGIDaemonProcess atmospi user=torpparit group=torpparit threads=5
    WSGIScriptAlias / $__WSGI_PATH

    <Directory $__ATMOSPI_DIR>
        Require all granted
    </Directory>

    <Directory $__ATMOSPI_MODULE_DIR>
        WSGIProcessGroup atmospi
        WSGIApplicationGroup %{GLOBAL}
    </Directory>
</VirtualHost>
EOF
echo Next: 'sudo ln -sf $PWD/000-atmospi.conf /etc/apache2/sites-enabled/'
