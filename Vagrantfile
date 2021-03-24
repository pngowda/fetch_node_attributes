
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/bionic64" 
  # access a port on your host machine (via localhost) and have all data forwarded to a port on the guest machine.
  config.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: true
  # Folders on your host machine to be synced to and from the guest machine
  config.vm.synced_folder './', '/vagrant'
  
  # Setting up corporate proxy if required  
  if Vagrant.has_plugin?("vagrant-proxyconf")
		config.proxy.http     = "http://proxy.example.com:8080"
		config.proxy.https    = "http://proxy.example.com:8080"
		config.proxy.no_proxy = "localhost,127.0.0.1"
	end
  config.vm.provider "virtualbox" do |vb|
    vb.name = 'docker-vm'
    vb.memory = 2048
    vb.cpus = 2
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  # Shell Provision
  config.vm.provision :shell, inline: "sudo apt-get update"
	
  # Shell Provision: 
  # This is a work around to get the exact host disk utilization details inside the container. 
  # otherwise the mount mount of a partition will differ.
  config.vm.provision :shell, inline: "df -h | grep '^/dev' > /vagrant/host_disk_info.txt"
  
  # Docker Provision
  config.vm.provision "docker" do |docker|
    build_image_args =  "-t node_info_image"
    if ENV.has_key?('http_proxy') && ENV.has_key?('https_proxy')
      build_image_args = build_image_args + " --build-arg http_proxy=" + ENV['http_proxy']
      build_image_args = build_image_args + " --build-arg https_proxy=" + ENV['https_proxy']
    end
	# Build docker image and run container
    docker.build_image "/vagrant/.", args: build_image_args
    docker.run "node_info_image", args: "-v '/vagrant:/vagrant'"
  end
end