#!/bin/bash

#This script makes several assumptions:
# 1. Running on a host with openstack client tools installed
# 2. Using a default ssh key in ~/.ssh/
# 3. The user knows what they're doing.
# 4. The user has read this script and asked the maintainers 
#    about any code that is not well commented or is unclear.
#    Or, is at the least, willing to gamble.

echo 'Creating Container Tutorial infrasturcture with hardcoded values!'

openrc_path="/home/jecoulte/Work/Tools/Jetstream_cli/openrc-files/openrc-staff.sh"

cluster_name="jec-tuttest"
volume_size=5
headnode_size="m1.small"

current_tutorial="SGCI2021"

source ${openrc_path}

if [[ ! -f ${openrc_path} ]]; then
  echo "openrc path: ${openrc_path} \n does not point to a file!"
  exit 1
fi

#Build a cluster:
if [[ -f ./${current_tutorial}_VC/cluster_create.sh ]]; then
  echo "Using existing clone of the VC repo"
else
  git clone --single-branch --branch cent8-update https://github.com/XSEDE/CRI_Jetstream_Cluster ${current_tutorial}_VC
fi
  
cd ./${current_tutorial}_VC
  
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


ssh centos@${cluster_ip} 'for user in train{01..99}; do sudo useradd $user; done'
ssh centos@${cluster_ip} 'for user in train{01..99}; do sudo usermod -aG docker $user; done'

#set user passwords!
scp user_list.txt centos@${cluster_ip}:
ssh centos@${cluster_ip} 'cat user_list.txt | sudo chpasswd'

#Allow sudo + singularity useage for building
scp singularity-sudoers centos@${cluster_ip}:
ssh centos@${cluster_ip} 'sudo cp singularity-sudoers /etc/sudoers.d/'

# Copy over files used in the exercises
ssh centos@${cluster_ip} 'sudo mkdir -p -m 777 /opt/ohpc/pub/examples'
scp ../${current_tutorial}/files/* centos@${cluster_ip}:/opt/ohpc/pub/examples/

#Now, create a script to test the commands in the current tutorial directory:
# At least for Day 1...
echo "#!/bin/bash" > ${current_tutorial}_test.sh
grep -hE '^\$|```\$' ../${current_tutorial}/Day1\ Ex\ 1\ Part\ * | tr -d '[\`]'  | sed 's/^\$ //' | grep -vE "singularity remote|singularity push" >> ${current_tutorial}_test.sh

#Fixes for specific problematic commands!
sed -i 's@echo 5 | docker run -i $USER/py3-dice@docker run -i $USER/py3-dice@' ${current_tutorial}_test.sh

sed -i 's/vim \.\/Dice.def/sed -i "s@\\\$USERNAME@\$USER@" Dice.def/' ${current_tutorial}_test.sh

sed -i 's/vim/#vim/' ${current_tutorial}_test.sh

chmod u+x ${current_tutorial}_test.sh

scp ${current_tutorial}_test.sh centos@${cluster_ip}:

echo "Running commands from EX1 now!"

ssh centos@${cluster_ip} "sudo cp ${current_tutorial}_test.sh /home/train99/ && sudo chown train99:train99 /home/train99/${current_tutorial}_test.sh && sudo su - train99 -c \"/home/train99/${current_tutorial}_test.sh > ${current_tutorial}_test_out.txt\" && sudo cp /home/train99/${current_tutorial}_test_out.txt /home/centos/"

scp centos@${cluster_ip}:${current_tutorial}_test_out.txt ./
