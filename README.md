# Dockerized tool to dispay node attributes in json format

This repo provides a template vagrantfile with docker provisioning which spins up a vm and run a dockerrized python tool to fetch node attributes.

Below are some of the node attributes being captured : 
- OS Info 
- CPU Count
- Memory Info,
- Disk partition and utilization.

Requirements
------------

* VirtualBox : https://www.virtualbox.org/wiki/Downloads
* Vagrant : https://www.vagrantup.com/downloads

Configure your corporate proxy
------------------------------

* Install [Proxy Configuration Plugin](http://tmatilai.github.io/vagrant-proxyconf/) for Vagrant if running behind corporate proxy:
  - vagrant plugin install vagrant-proxyconf
    Confgure Vagrantfile with:
    ```
  	Vagrant.configure("2") do |config|
		if Vagrant.has_plugin?("vagrant-proxyconf")
			config.proxy.http     = "http://proxy.example.com:8080"
			config.proxy.https    = "http://proxy.example.com:8080"
			config.proxy.no_proxy = "localhost,127.0.0.1"
		end
	end
     ```
* Add environment variables:
  - export/set http_proxy=http://proxy.example.com:8080
  - export/set https_proxy=http://proxy.example.com:8080

Run the application
-------------------

- ```vagrant up ```: Spins up a Ubuntu bionic VM with 2 Gb RAM and 2 CPUs.

- ```vagrant provision``` : Shell provisioning to update apt and Docker provisioning to install docker and build/run the docker image.

Expected Result
---------------

Json file (node_attribute_information.json) with node attribute details gets created in the checkedout directory and this will be overwritten for every docker run.
e.g output:
   ```
   {
    "OS": [
        {
            "Operating System": "Linux",
            "Release": "4.15.0-137-generic",
            "Version": "#141-Ubuntu SMP Fri Feb 19 13:46:27 UTC 2021"
        }
    ],
    "CPU": [
        {
            "Physical cores": 2,
            "Total cores": 2
        }
    ],
    "MEMORY": [
        {
            "VIRTUAL_MEMORY": {
                "Total": "1.95GB",
                "Available": "1.60GB",
                "Used": "190.85MB",
                "Percentage": 17.7
            }
        },
     ........
   ```
