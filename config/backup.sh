#!/bin/bash  
echo "Begin Shutting down Swahilipot Odoo containers"
cd /opt/odoo_erp/ && docker-compose down
echo "Successfully shut down containers"

echo "Backup Database data"
docker run -v odoo_erp_db:/volume --rm --log-driver none loomchild/volume-backup backup -v -c gz - > /opt/docker_volume_backups/$(date "+%Y_%m_%d_%H_%M_%S")_odoo_erp_db.tar.gz
echo "Successfully backed up Database data"

echo "Backup Odoo web data"
docker run -v odoo_erp_web:/volume --rm --log-driver none loomchild/volume-backup backup -v -c gz - > /opt/docker_volume_backups/$(date "+%Y_%m_%d_%H_%M_%S")_odoo_erp_web.tar.gz
echo "Successfully backed up Odoo Web data"

echo "Restart Greenwood containers"
cd /opt/odoo_erp/ && docker-compose up -d
echo "System is up and running"
