#!/usr/bin/fish
set -l __WSGI_PATH "$PWD/atmospi.wsgi"
set -l __ATMOSPI_DIR $PWD
set -l __ATMOSPI_MODULE_DIR "$__ATMOSPI_DIR/Atmospi"
set -l __ATMOSPI_CONF 000-(basename $PWD).conf
rm $__ATMOSPI_CONF ^&1
echo -n "<VirtualHost *:80>
    ServerName atmospi
    ServerAlias atmospi1 atmospi2 atmospi3 atmospi4 atmospi5 atmospi6 atmospi7 atmospi8 atmospi9 atmospi10

    WSGIDaemonProcess atmospi user=$USER group=$USER threads=5
    WSGIScriptAlias / $__WSGI_PATH

    <Directory $__ATMOSPI_DIR>
        Require all granted
    </Directory>

    <Directory $__ATMOSPI_MODULE_DIR>
        WSGIProcessGroup atmospi
        WSGIApplicationGroup %{GLOBAL}
    </Directory>
</VirtualHost>" > $__ATMOSPI_CONF
echo Next: "sudo ln -sf \$PWD/$__ATMOSPI_CONF /etc/apache2/sites-enabled/"
