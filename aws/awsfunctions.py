import boto.ec2

def power(key,secret,ins,action,region):
    r = boto.ec2.get_region(region)
    conn = boto.connect_ec2(key,secret,region=r)
    reservations = conn.get_all_instances(filters={"instance_id":ins})
    selected_id=reservations[0].instances[0]
    response=""
    if action == "Start" and (selected_id._state.name)=="stopped":
        try:
            selected_id.start()
            response="success"
        except Exception as e:
            response=e.message
        return response

    elif action == "Stop" and (selected_id._state.name)=="running":
        try:
            selected_id.stop()
        except Exception as e:
            response=e.message
            return response

    elif action == "Reboot" and (selected_id._state.name)=="running":
        try:
            selected_id.reboot()
        except Exception as e:
            response=e.message
            return response

    else:
        response=("Instance is '" + selected_id._state.name + "' and action '" +action + "' can not be executed")
    return response