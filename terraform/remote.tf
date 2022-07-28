resource "null_resource" "remote"{
connection {
       type = "ssh"
       user = "ubuntu" #standart user for ubuntu machine
       private_key = var.ssh_access_key
       host  = aws_instance.app_server.public_ip #get ip from EC2 instance
}

# Copies the file
provisioner "file" {
  source      = "${path.module}/docker-compose.yml" #provide neccesary files
  destination = "docker-compose.yml" #destination of files
}

provisioner "file" {
  source      = "${path.module}/install-docker.sh" #provide neccesary files
  destination = "/tmp/install-docker.sh" #destination of files
}

provisioner "file" {
  source      = "${path.root}/../backend" #provide neccesary files
  destination = "/tmp/backend" #destination of files
}

provisioner "file" {
  source      = "${path.root}/../frontend" #provide neccesary files
  destination = "/tmp/frontend_vol" #destination of files
}

provisioner "file" {
  destination = ".env" #destination of files
  content = templatefile("${path.module}/env.tftpl",
  {
  postgres_user = var.postgres_user
  postgres_password = var.postgres_password
  db_name = var.db_name
  secret_key = var.secret_key
  client_secret = var.client_secret
  signing_secret = var.signing_secret
  bot_user_oauth_token = var.bot_user_oauth_token
  frontend_docker_image = var.frontend_docker_image
  backend_docker_image = var.backend_docker_image
   })
}

provisioner "file" {
  destination = ".default.conf" #destination of files
  content = templatefile("${path.module}/default.conf.tftpl",
  {
    server_ip = aws_instance.app_server.public_ip
   })
}

provisioner "remote-exec" {
         inline = [
                    "export $(grep -v '^#' .env | xargs -0) && echo $POSTGRES_USER",
                    "sudo mv -v /tmp/backend /tmp/frontend_vol ~",
                    "chmod +x /tmp/install-docker.sh",
                    "/tmp/install-docker.sh",
                    "sudo docker login --username=${var.docker_user} --password=${var.docker_token}",
                    "sudo docker-compose up -d --force-recreate",
                  ]
  }
}
