# aws-monitor
0. My local system is Windows while the ec2 instance I created is Amazon Linux AMI.

1. To configure the installation on the local system, run installation.bat with cmd. (But currently my credentials are removed from that file)

2. The python script check_status.py takes 3 command line arguments, which stand for cpu_limit, networe_limit and memory_limit respectively. The script will check if the maximum value in the past hour exceeds the limit.
   
3. To simulate server overload situation, simply run "python check_status.py 0 0 0" in cmd.

4. If a server is overloaded, the script will 1)create a new instance, 2)create a new elastic ip 3)wait for 2 minutes for the new instance to be initialized, 4)associate the elastic ip with the new instance, 5)update route53, 6)send an email to a user, which in this case is bertrand.y@hotmail.com

5. To make the vertual machine send memory metrics, I used an open source code https://gist.github.com/shevron/6204349. I sshed to the Linux AMI using puTTY, and run the script in the virtual machine.
   There is also another way of doing so in the official documentation. http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/mon-scripts.html
