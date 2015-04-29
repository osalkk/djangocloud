
import boto.ec2,json
import cgi,cgitb
import boto.ec2.cloudwatch
import time,datetime
import logging
import logging.handlers
from datetime import  timedelta

logger = logging.getLogger()
fh = logging.FileHandler('/tmp/django.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)


def connect(key,secret,region):

    #print(key,secret)
    r = boto.ec2.get_region(region)
    conn = boto.connect_ec2(key,secret,region=r)
    conn_cloudwatch=boto.ec2.cloudwatch.connect_to_region(region,aws_access_key_id=key,aws_secret_access_key=secret)

    response=[]
    try:
        res = conn.get_all_instances()

        if res:

            for instance in res:
                dic1={}

                for inst in instance.instances:
                    reservations = conn.get_all_instances(filters={"instance_id":inst.id})
                    #reservations = conn.get_all_instances()
                    if ("Name" in inst.tags):
                        inst_name = reservations[0].instances[0].tags['Name']
                        inst_state = reservations[0].instances[0].state
                        inst_type = reservations[0].instances[0].instance_type
                        inst_id = reservations[0].instances[0].id
                        inst_placement=reservations[0].instances[0].placement

                    else:
                        inst_name = reservations[0].instances[0].id
                        inst_state= reservations[0].instances[0].state
                        inst_type= reservations[0].instances[0].instance_type
                        inst_id = reservations[0].instances[0].id
                        inst_placement=reservations[0].instances[0].placement

                dic1["Name"] = inst_name
                dic1["Status"] = inst_state
                dic1["Id"] = inst_id
                dic1["Type"] = inst_type
                dic1["AZ"] = inst_placement

                response.append(dic1)

    except Exception as e:

            response=e.message


    return response
def connect1(instance_id,key,secret,region):
    logger.info("connect1 istendi")
    logger.info(instance_id)
    r = boto.ec2.get_region(region)
    conn = boto.connect_ec2(key,secret,region=r)
    conn_cloudwatch=boto.ec2.cloudwatch.connect_to_region(region,aws_access_key_id=key,aws_secret_access_key=secret)
    response=[]
    res = conn.get_all_instances(filters={"instance_id":instance_id})
    logger.info(res)
    for instance in res:
        dic1={}

        volume_list=[]
        snap_list=[]
        for inst in instance.instances:
            reservations = conn.get_all_instances(filters={"instance_id":inst.id})
            #reservations = conn.get_all_instances()
            if ("Name" in inst.tags):
                inst_name = reservations[0].instances[0].tags['Name']
                inst_state = reservations[0].instances[0].state
                inst_type = reservations[0].instances[0].instance_type
                inst_id = reservations[0].instances[0].id
                inst_placement=reservations[0].instances[0].placement
                inst_private_ip=reservations[0].instances[0].private_ip_address
                inst_public_ip=reservations[0].instances[0].ip_address
                volumes = conn.get_all_volumes(filters={'attachment.instance-id': inst_id})
                alarm_dimensions = {'InstanceId':[inst_id]}
                owner_id=reservations[0].owner_id
                print(owner_id)
                for volume in volumes:


                    snapshots = conn.get_all_snapshots(filters={'volume-id': volume.id})
                    for i in range(len(snapshots)):
                        snaps={}
                        snaps['snapid']=snapshots[i].id
                        snaps['snapvolume']=snapshots[i].volume_id
                        snaps['snapdesc']=snapshots[i].description
                        snap_list.append(snaps)


                if inst_state!='stopped':
                    ins_cpu=conn_cloudwatch.get_metric_statistics(300,datetime.datetime.utcnow()-datetime.timedelta(seconds=600),datetime.datetime.utcnow(),'CPUUtilization','AWS/EC2','Average',dimensions=alarm_dimensions)
                    ins_networkin=conn_cloudwatch.get_metric_statistics(300,datetime.datetime.utcnow()-datetime.timedelta(seconds=600),datetime.datetime.utcnow(),'NetworkIn','AWS/EC2','Average',dimensions=alarm_dimensions)
                    ins_networkout=conn_cloudwatch.get_metric_statistics(300,datetime.datetime.utcnow()-datetime.timedelta(seconds=600),datetime.datetime.utcnow(),'NetworkOut','AWS/EC2','Average',dimensions=alarm_dimensions)
                    ins_diskread=conn_cloudwatch.get_metric_statistics(300,datetime.datetime.utcnow()-datetime.timedelta(seconds=600),datetime.datetime.utcnow(),'DiskReadBytes','AWS/EC2','Average',dimensions=alarm_dimensions)
                    ins_diskwrite=conn_cloudwatch.get_metric_statistics(300,datetime.datetime.utcnow()-datetime.timedelta(seconds=600),datetime.datetime.utcnow(),'DiskWriteBytes','AWS/EC2','Average',dimensions=alarm_dimensions)
                    print('networkin')
                    for asd in ins_networkin:
                        print(asd['Average'])
                    print('#############')
                    print('networkout')
                    for asd in ins_networkout:
                        print(asd['Average'])


                    cpu=round(ins_cpu[:1][0]['Average'],0)
                    networkin=round(ins_networkin[:1][0]['Average'],2)/1048576
                    networkout=round(ins_networkout[:1][0]['Average'],2)/1048576
                    diskread=round(ins_diskread[:1][0]['Average'],2)/1024
                    diskwrite=round(ins_diskwrite[:1][0]['Average'],2)/1024

                else:
                    cpu=0
                    networkin=0
                    networkout=0
                    diskread=0
                    diskwrite=0

                for i in range(len(volumes)):
                    vols={}
                    vols["volname"]=str(volumes[i].id)
                    vols["volsize"]=str(volumes[i].size)
                    vols["voldevice"]=str(volumes[i].attach_data.device)
                    volume_list.append(vols)



            else:
                inst_name = reservations[0].instances[0].id
                inst_state= reservations[0].instances[0].state
                inst_type= reservations[0].instances[0].instance_type
                inst_id = reservations[0].instances[0].id
                inst_placement=reservations[0].instances[0].placement
                inst_private_ip=reservations[0].instances[0].private_ip_address
                inst_public_ip=reservations[0].instances[0].ip_address
                volumes = conn.get_all_volumes(filters={'attachment.instance-id': inst_id})
                if inst_state!='stopped':
                    ins_cpu=conn_cloudwatch.get_metric_statistics(300,datetime.datetime.utcnow()-datetime.timedelta(seconds=600),datetime.datetime.utcnow(),'CPUUtilization','AWS/EC2','Average',dimensions=alarm_dimensions)
                    ins_networkin=conn_cloudwatch.get_metric_statistics(300,datetime.datetime.utcnow()-datetime.timedelta(seconds=3600),datetime.datetime.utcnow(),'NetworkIn','AWS/EC2','Average',dimensions=alarm_dimensions)
                    ins_networkout=conn_cloudwatch.get_metric_statistics(300,datetime.datetime.utcnow()-datetime.timedelta(seconds=3600),datetime.datetime.utcnow(),'NetworkOut','AWS/EC2','Average',dimensions=alarm_dimensions)
                    ins_diskread=conn_cloudwatch.get_metric_statistics(300,datetime.datetime.utcnow()-datetime.timedelta(seconds=3600),datetime.datetime.utcnow(),'DiskReadBytes','AWS/EC2','Average',dimensions=alarm_dimensions)
                    ins_diskwrite=conn_cloudwatch.get_metric_statistics(300,datetime.datetime.utcnow()-datetime.timedelta(seconds=3600),datetime.datetime.utcnow(),'DiskWriteBytes','AWS/EC2','Average',dimensions=alarm_dimensions)
                    cpu=round(ins_cpu[:1][0]['Average'],0)
                    networkin=round(ins_networkin[:1][0]['Average'],0)/1048576
                    networkout=round(ins_networkout[:1][0]['Average'],0)/1048576
                    diskread=round(ins_diskread[:1][0]['Average'],0)/1048576
                    diskwrite=round(ins_diskwrite[:1][0]['Average'],0)/1048576

                else:
                    cpu=0
                    networkin=0
                    networkout=0
                    diskread=0
                    diskwrite=0

                for i in range(len(volumes)):
                    vols={}
                    vols["volname"]=str(volumes[i].id)
                    vols["volsize"]=str(volumes[i].size)
                    vols["voldevice"]=str(volumes[i].attach_data.device)
                    volume_list.append(vols)


        dic1["Name"] = inst_name
        dic1["Status"] = inst_state
        dic1["Id"] = inst_id
        dic1["Type"] = inst_type
        dic1["AZ"] = inst_placement
        dic1["private"] = inst_private_ip
        dic1["public"] = inst_public_ip
        dic1["volumes"] = volume_list
        dic1["cpu"] = cpu
        dic1["networkin"] = networkin
        dic1["networkout"] = networkout
        dic1["diskread"] = diskread
        dic1["diskwrite"] = diskwrite
        dic1["snapshots"] = snap_list

        response.append(dic1)



    return response

def vol(key,secret,instance_id,region,volume_name):
    print(key,secret,instance_id,region,volume_name)
    response=[]
    r = boto.ec2.get_region(region)
    conn = boto.connect_ec2(key,secret,region=r)
    volumes = conn.get_all_volumes(filters={'attachment.instance-id': instance_id})
    print(volumes)
    dic1={}
    for volume in volumes:
        snap_list=[]
        snapshots = conn.get_all_snapshots(filters={'volume-id': volume.id})
        for i in range(len(snapshots)):
            snaps={}
            print(snapshots[i])
            snaps['snapid']=snapshots[i].id
            snaps['snapvolume']=snapshots[i].volume_id
            snaps['snapdesc']=snapshots[i].description
            snaps['snapdate']=snapshots[i].start_time
            snap_list.append(snaps)


    dic1["snapshots"] = snap_list

    response.append(dic1)



    return json.dumps(snap_list)


def connect_all(key,secret):


    #print(key,secret)
    region_list=['eu-west-1','eu-central-1']

    response1=[]
    for region in region_list:
        #print(region)
        response={}
        r = boto.ec2.get_region(region)
        conn = boto.connect_ec2(key,secret,region=r)

        try:
            res = conn.get_all_instances()

            count=len(res)
            response['region']=region
            response['count']=count


        except Exception as e:

            response=e.message
            return response

        response1.append(response)





    return response1



if __name__ == "__main__":
    try:
        
        vol(key,secret,instance_id,region,volume_name)
    except:
        cgi.print_exception()