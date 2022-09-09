
# Terraform
Run in Terminal

 `wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg`
 `echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list`

 `sudo apt update && sudo apt install terraform`
 
 ### What is Terraform?
  * open source tool by Hashicorp, used for providing infrasture resources.
  * supports DEVOPS best practices for change management
  * Managing configuration files in source control to mainatian an idela provisioning state fro testing and production

  We need the terraform client 
   and **files** are :

   * `main.tf`
   * `variables.tf`
   * Optional ` resources.tf`
   ,`output.tf`, `tfstate`


   How to define configuration of resources in your terraform files?

   # **GOOGLE CLOUD**
---
## How to setup an environment in Google Cloud

Before we create an instance, we need to generate an SSH key. The key will then be used to generate an instance of the VM.

https://cloud.google.com/compute/docs/connect/create-ssh-keys

Run in git bash terminal

* `ssh-keygen -t rsa -f ~/.ssh/gcp -C leviscoffie -b 2048`

* You get the private key and public key
Input this public key to google cloud consloe.

* copy the ssh key `cat.gcp`

* All instances in this project inherit these SSH keys. 

* Click create an intannce and input all the relevant features
* you can pull down the instance any time you are not using it to save on server costs.

* Copy external IP

Go to terminal and input `ssh -i ~/.ssh/gcp leviscoffie@34.65.209.138`

`htop` to check specs of the virtual machine we have created.


Download anaconda to this instance and the type `bash Anaconda3-2022.05-Linux-x86_64.sh` to run it and while it installs, open anothr terminsl and cd into ssh folder where you will create a `config ` folder using ` touch config`
* Cofigure the file 
  `  Host de-zoomcamp
    HostName 34.65.209.138
    User leviscoffie
    IdentityFile ~/leviscoffie/.ssh/gcp
  `

### How to config the virtual machine to use VSCode which is our usual machine

Download Remote-SSH and the click on bottom let corner where there is _open a remote window_
* Choose the host _de-z00camp_ which has already been configured above.


* Executable files show green in terminal and thus you can make execute using  `chmod +x /NAME OF FILE/`

* Now when you dont want to keep going to the bin directory. we can make it visible from any directory  and thus we  need to add docker compose to the path variable.

* We then open the bashrc file using `nano`.

* Go to the end and add /bin dir to the PATH
`export PATH="${HOME}/bin:${PATH}` --does not change path just prepends the bin direcory with executble files to the [PATH]

* We use `source .bashrc` to logout and login to the bashrc terminal not you can do this from any directory.


* pgcli -h localhost -U root -d ny_taxi