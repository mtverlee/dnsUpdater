![digitalocean](https://www.underconsideration.com/brandnew/archives/digitalocean_logo.png "Digital Ocean")


# dnsUpdater
Small DNS updater to keep Digital Ocean domain records up to date with a DDNS. This code uses ipify.org to get the public IPv4 address of the local machine and updates a given Digital Ocean record.

### Note:
- **Currently this project only supports A records with IPv4 addresses.**

## Usage:
- Meant to be ran periodically on a cron timer.
### Syntax:
- ```--domain``` or ```-d``` - Domain to update on
- ```--record``` or ```-r``` - Record to update on domain
- ```--key``` or ```-k``` - Digital Ocean API key (get a key [here](https://cloud.digitalocean.com/settings/api/tokens))
- ```--allownew``` or ```-c``` - Allow new record to be created if it doesn't exist
- ```--verbose``` or ```-v``` - increase logging verbosity (log is written to install directory)

## Installation:
- ```apt update```
- ```apt install python python-pip```
- ```git clone https://github.com/mtverlee/dnsUpdater```
- ```cd dnsUpdater```
- ```pip install -r requirements.txt```
- ```python updater.py --domain <domain> --record <record> --key <key> --verbosity```

### Questions/Issues/Contibutions:
- Please feel free to file issues or create pull requests! All input is welcome.
