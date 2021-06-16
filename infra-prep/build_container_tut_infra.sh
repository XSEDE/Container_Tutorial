#!/bin/bash

#This script makes several assumptions:
# 1. Running on a host with openstack client tools installed
# 2. Using a default ssh key in ~/.ssh/
# 3. The user knows what they're doing.
# 4. The user has read this script and asked the maintainers 
#    about any code that is not well commented or is unclear.
#    Or, is at the least, willing to gamble.

openrc_path="<path-to-your-openrc-file>"

cluster_name="tutorial-test"
volume_size=5
headnode_size="m1.small"

current_tutorial="Gateways2020"

source ${openrc_path}

if [[ ! -f ${openrc_path} ]]; then
  echo "openrc path: ${openrc_path} \n does not point to a file!"
  exit 1
fi

#Build a cluster:
if [[ -f ./tut_VC/cluster_create.sh ]]; then
  echo "Using existing clone of the VC repo"
else
  git clone --single-branch --branch cent8-update https://github.com/XSEDE/CRI_Jetstream_Cluster tut_VC
fi
  
cd ./tut_VC
  
./cluster_create.sh -n ${cluster_name} -s ${headnode_size} -v ${volume_size} -o ${openrc_path} -d > cluster_build_output.txt

cluster_ip=$(tail -n 1 cluster_build_output.txt | sed 's/.*at \([0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\).*/\1/')

echo "Creating users on headnode: ${cluster_ip}"

cd .. #back to workingdir

#Create a list of training users w/ passwords
if [[ -f ./user_list.txt ]]; then
  echo "Using existing userlist in ./user_list.txt"
else
  for trainuser in train{01..99}; do
    echo "${trainuser}:$(cat /dev/urandom | tr -dc [:alnum:] | fold -w 8 | head -n 1)" >> user_list.txt
  done
fi

scp user_list.txt centos@${cluster_ip}:

ssh centos@${cluster_ip} 'for user in train{01..99}; do sudo useradd $user; done'
ssh centos@${cluster_ip} 'for user in train{01..99}; do sudo usermod -aG docker $user; done'
#What about needing sudo privileges with Singularity?!
ssh centos@${cluster_ip} 'cat user_list.txt | sudo chpasswd'

# NEED TO SPIT OUT FILES FOR THE CONTAINER TUTORIAL LIKE dice.py, etc.
ssh centos@${cluster_ip} 'sudo mkdir -p -m 755 /opt/ohpc/pub/examples'
scp ./${current_tutorial}/files/* centos@${cluster_ip}:/opt/ohpc/pub/examples/

#Now, create a script to test the commands in the current tutorial directory:
# At least for Day 1...
cd ${current_tutorial}
echo "#!/bin/bash" > EX_test_script.sh
grep -hE '^\$|```\$' Day1\ Ex\ 1\ Part\ * | tr -d '[\`\$]'  | sed 's/^ //' >> EX_test_script
chmod u+x EX_test_script.sh

scp EX_test_script.sh centos@${cluster_ip}:

echo "Running commands from EX1 now!"

ssh centos@${cluster_ip} 'sudo cp EX_test_script.sh /home/train99/ && sudo chown train99:train99 /home/train99/EX_test_script.sh && sudo su - train99 -c "/home/train99/EX_test_script.sh > EX_test_output.txt" && sudo cp /home/train99/EX_test_output.txt /home/centos/'

scp centos@${cluster_ip}:EX_test_output.txt ./
