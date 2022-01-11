# Configuraciones básicas para el funcionamineto de BIND9 en ubuntu server 20.04 LTS 
Vamos a configurar una ip estática a nuestro servidor en /etc/netplan/"nombre_del_archivo_de_configuración.yaml"

editaremos el archivo /etc/hosts

Se conocerán los archivos intervenidos para poner a punto el servicio de bind9
los archivos son los siguientes: 

Las configuraciones ya están apunto y el servicio se esta ejecutando sin errores

# contenido del archivo named.conf.local
## $ cat /etc/bind/named.conf.local

//zona directa para el dominio serverdns.com
zone "serverdns.com"{
  type master;
  file "/etc/bind/db.serverdns.com";
};

//zona inversa para la red 192.168.1.1
zone "1.168.192.in-addr.arpa"{
  type master;
  file "/etc/bind/db.1.168.192";
};


# contenido del archivo named.conf.options
## $ cat /etc/bind/named.conf.options
options {
        directory "/var/cache/bind";

        // If there is a firewall between you and nameservers you want
        // to talk to, you may need to fix the firewall to allow multiple
        // ports to talk.  See http://www.kb.cert.org/vuls/id/800113

        // If your ISP provided one or more IP addresses for stable
        // nameservers, you probably want to use them as forwarders.
        // Uncomment the following block, and insert the addresses replacing
        // the all-0's placeholder.

        // forwarders {
        //      0.0.0.0;
        // };

        //========================================================================
        // If BIND logs error messages about the root key being expired,
        // you will need to update your keys.  See https://www.isc.org/bind-keys
        //========================================================================
        dnssec-validation auto;

        listen-on-v6 { any; };
};


# contenido del archivo named.conf.defaults-zones
## $ cat /etc/bind/named.conf.default-zones
// prime the server with knowledge of the root servers
zone "." {
        type hint;
        file "/usr/share/dns/root.hints";
};

// be authoritative for the localhost forward and reverse zones, and for
// broadcast zones as per RFC 1912

zone "localhost" {
        type master;
        file "/etc/bind/db.local";
};

zone "127.in-addr.arpa" {
        type master;
        file "/etc/bind/db.127";
};

zone "0.in-addr.arpa" {
        type master;
        file "/etc/bind/db.0";
};

zone "255.in-addr.arpa" {
        type master;
        file "/etc/bind/db.255";
};


# contenido de la base de datos para la zona directa - archivo db.serverdns.com
## $ cat /etc/bind/db.serverdns.com
;
; BIND data file for local loopback interface
;
$TTL    604800
@       IN      SOA     ubuntu.serverdns.com. root.serverdns.com. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@        IN     NS      ubuntu.serverdns.com.
ubuntu   IN     A       192.168.1.117
monitor  IN     A       192.168.1.102


# contenido de la base de datos para la zona inverza - archivo db.1.168.192
## $ cat /etc/bind/db.1.168.192
;
; BIND reverse data file for local loopback interface
;
$TTL    604800
@       IN      SOA     ubuntu.serverdns.com. root.serverdns.com. (
                              1         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      ubuntu.serverdns.com.
117     IN      PTR     ubuntu.serverdns.com.
102     IN      PTR     monitor.serverdns.com.



# se modificó el archivo /etc/hosts comentando la primera linea del archivo y añadiendo el FQDN de la máquina anfitrión
## $ cat /etc/hosts
#127.0.0.1 localhost
192.168.1.117 ubuntu.serverdns.com ubuntu

#The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts


#  contenido de arvicho de configuración de red con /etc/netplan
## $ cat /etc/netplan/50-cloud-init.yaml
#This file is generated from information provided by the datasource.  Changes
#to it will not persist across an instance reboot.  To disable cloud-init's
#network configuration capabilities, write a file
#/etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
#network: {config: disabled}
network:
    version: 2
    renderer: networkd
    ethernets:
        eth0:
          addresses: [192.168.1.117/24]
          gateway4: 192.168.1.1
          nameservers:
            search: [serverdns.com]
            addresses: [8.8.8.8, 8.8.4.4]
//            dhcp4: true
//            optional: true

seguimos avanzando... -_-




