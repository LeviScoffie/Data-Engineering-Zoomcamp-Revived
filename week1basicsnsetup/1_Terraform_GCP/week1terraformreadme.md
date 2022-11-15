
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

## **CONFIGURING VM INSTANCE**


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

#### **BASHRC**

* Use command `less .bashrc` - a file that is executed everytime we log into the virtual machine

* `source .bashrc`


### Configuring VSCODE to Access VM instance

* In extensions download _remote-ssh_
* Click on open a remote window at the far bottom left of vscode screen.
* Select connect to host, and since we has already defined the host in our config file we then shoould be able to be given the option of out virtual machine which de-zoomcamp.

* meanwhile you can install docker and docker compile to the virtual machine instance.
    * Afterwards install docker compose. go to their github and select releases.
    * Select the one for linux (according to your virtual machine)

* You can then clone the project repo into the ssh remote connection interface.

* Use HTTPS innsted of SSH when  cloning because its an anon way of chechking out a repo.

* IN the root of the vm create a folder called bin. This is the folder that contains  all the executable files and where docker compose sshould reside. `mkdir bin` Then... cd into it.

* Use `wget https://github.com/docker/compose/releases/download/v2.11.0/docker-compose-linux-x86_64` to download the docker into the bin exec file.

* Executable files show green in terminal and thus you can make executable using  `chmod +x /NAME OF FILE/`

* Now when you dont want to keep going to the bin directory. we can make it visible from any directory  and thus we  need to add docker compose to the path variable.

* We then open the bashrc file using `nano`.

* Go to the end and add /bin dir to the PATH
`export PATH="${HOME}/bin:${PATH}` --does not change path just prepends the bin direcory with executble files to the [PATH]

* We use `source .bashrc` to logout and login to the bashrc terminal not you can do this from any directory.

* Therefore that can be done from any directory.
 ### ** Working on the Repo Files**
* CD into 2_docker_sql where there is a docker compose yaml file. and run the just installed docker compose there.

* Run docker-compose up -d (detach mode)

* Now install pgcli 
`pip install pgcli`
can also use conda to install it  `conda install -c conda-forge pgcli`


* pgcli -h localhost -U root -d ny_taxi _as was the previous time we were updating database_


### **Accessing Postgres. Forwading the Port to Local Machine**
 * Acess postgres install locally. On the ssh remote connection.Open terminial and click port.

 * Forward the postgres port that to ssh that is _5432_ also forward the pgadmin port _8080_.

 * And now we will be able to access these ports from out local machine.

 * Open another terminal not the vm one and input the pgcli command 
 `pgcli -h localhost -U root -d ny_taxi`
  And now u can access this postgres instacne from your local machine. (Forwading from the ssh remote instance to local machine)


  ### Executing the Jupyter Notebook in 2_docker_sql

  * cd into it and run `jupyter notebook` the forward another port `8888`.
  * Got to the **week1basicsnsetup/2_docker_sql/update-data-2.ipynb** file and download the data once more.
  

  ### Terraform Install

  `wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg`

`echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list`

`sudo apt update && sudo apt install terraform`

If you dont want to download it with a package manager you can just download it as binary.

* `wget https://releases.hashicorp.com/terraform/1.2.9/terraform_1.2.9_linux_amd64.zip` while in the bin directory

* It will come as a zip file... use `unzip` after installing unzip in sudo apt.

Bin is already on our path variable folder and hence it is discoverable..test with `terraform --version`

After cd  into terraform we now need our GCP service account json credentials. we need to this json file file to communicate with the server.

* We therefore use `sftp de-zoomcamp` for transferring the json file. in the directory which it is located in your local machine.

* Once connected `mkdir` and the cd into which then `put the json file`

## Configuring Our GOOGLECLOUD CLI

A remote instance like this requires 
 we use another method of authentiction

 ### Setting Up Google Application credentials 
 
 - export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/loyal-glass-359906-d8498db322d5.json

* Now to use the json file to authenicate out CLI

 gcloud auth activate-service-account --key-file
 $GOOGLE_APPLICATION_CREDENTIALS

 its shows this ```bash Activated service account credentials for: [taxi-rides-ny@loyal-glass-359906.iam.gserviceaccount.com]
 ```

 * terraform init
 * terrafrom plan