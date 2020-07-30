#!/bin/bash

runfile="test_run.sh"

echo '#!/bin/bash' > test_run.sh
echo "export USERNAME=$USER" >> test_run.sh
echo "export GITHUB_USERNAME=ECoulter" >> test_run.sh
echo "export COLLECTION_NAME=tutorial-containers" >> test_run.sh

grep '\$ ' exercise1.md | grep -v "remote login" | grep -v "push" >> test_run.sh

sed -i 's/```//g' test_run.sh

sed -i 's/\$ //g' test_run.sh

#write sed commands for the vim edits people have to do
# vim slurm_dice.job
sed -i 's/vim .\/Dice.def/sed -i "s\/\\\$USERNAME\/$USERNAME\/g" Dice.def/' test_run.sh
sed -i '/vim slurm_dice.job/d' test_run.sh

sed -i '/cat dice_test_63.out/d' test_run.sh

#cp the .singularity remote auth file from /home/centos/.singularity/ to test the push

chmod u+x test_run.sh

