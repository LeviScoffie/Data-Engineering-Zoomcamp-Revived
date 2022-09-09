
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