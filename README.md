# MicasenseNBIVisualize
This project use Micasence MX30 image to calculate NBI.

Hosting in nuc on UAV
connect to nuc wifi 
and go to 10.42.0.1:5000
Detail control instruction please check NBI程式使用說明.docx

## install dependency:

run install_dependency.bat to install dependency

```
install_dependency.bat
```

## Starting point
```
python3 Server.py

```

## setup hotspot 
```
nmcli con show
nmcli con mod <connection-name> connection.autoconnect yes

```


