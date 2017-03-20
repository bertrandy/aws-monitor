
from sys import argv
import boto
import datetime
import boto.ec2.cloudwatch

def check_status(cpu_limit,network_limit,memory_limitS):

  instance_id = 'i-02e46274432aef2e9'	
  region = 'us-east-1'
  cw = boto.ec2.cloudwatch.connect_to_region(region)

  #set monitor time
  end = datetime.datetime.utcnow()
  start = end - datetime.timedelta(seconds = 3600)

  #check cpu usage
  metric1 = cw.list_metrics(dimensions={'InstanceId':instance_id},metric_name= 'CPUUtilization')[0]
  datapoints1 = metric1.query(start, end, 'Maximum', 'Percent',period = 60)
  d1 = datapoints1[0]
  cpu_load = d1['Maximum']
  print "cpu_load"
  print cpu_load

  #check network usage
  metric2 = cw.list_metrics(dimensions={'InstanceId':instance_id},metric_name= 'NetworkOut')[0]
  datapoints2 = metric2.query(start, end, 'Maximum', 'Bytes',period = 60)
  d2 = datapoints2[0]
  network_load = d2['Maximum']
  print "network_load"
  print network_load
  
  
  #check memory usage
  #this requires the virtual machine to send out custom metrics "EC2/Memory"
  #I used an open source code to do that
  metric3 = cw.list_metrics(dimensions={'InstanceId':instance_id},metric_name= 'EC2/Memory')[0]
  datapoints3 = metric3.query(start, end, 'Maximum', 'Percent',period = 60)
  d3 = datapoints3[0]
  memory_load = d3['Maximum']
  print "memory_load"
  print memory_load  
  

  if cpu_load<cpu_load and network_load<network_limit and memory_load<memory_limit :
    return True;
  else:
    return False;

 
def response():
  #create another EC2 instance
  import boto
  conn = boto.connect_ec2()
  image_id = 'ami-188d6e0e'
  reservation = conn.run_instances(image_id)  
  instance = reservation.instances[0]
  new_id = instance.__dict__['id']
  

  #create elastic ip
  new_conn = boto.ec2.connection.EC2Connection()
  new_eip = new_conn.allocate_address()
  import time
  time.sleep(120) #wait till instance is initiated
  new_eip.associate(instance_id=new_id)
  

  #update route53
  import boto.route53
  conn53 = boto.connect_route53()
  zone = conn53.get_zone("junran-yang.net")
  changes = boto.route53.record.ResourceRecordSets(conn53, zone.id)
  change = changes.add_change("UPSERT", "www.junran-yang.net", "A")
  change.add_value("52.86.187.46")
  change.add_value(new_eip)
  result = changes.commit()
  

  #send email    
  import boto.ses
  conn = boto.ses.connect_to_region('us-east-1')
  conn.send_email(
          'junran.y@hotmail.com',
          'Server Overloaded',
          'server is overloaded',
          'bertrand.y@hotmail.com')

def main():
  if len(argv) != 4:
    print "invalid arguments" 
  else:
    status = check_status(argv[1],argv[2],argv[3])
    if not status:
      response()

if __name__ == '__main__':
  main()


