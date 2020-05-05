import random 
import builtins

from flask import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\dasdasdn\xec]/'

manager = builtins.manager

@app.route('/')
def landing_page():
    return render_template('home.html')

# Return the Devices in HTML Format
@app.route('/devices')
def devices():
    response = manager.list_devices()
    return render_template('devices.html', devices=response)

# Return the Groups in HTML Format
@app.route('/groups')
def groups():
    response = manager.list_groups()
    return render_template('groups.html', groups=response)

# Return the dtypes in HTML Format
@app.route('/dtypes')
def dtypes():
    response = manager.list_dtypes()
    return render_template('groups.html', groups=response)

# Return the Devices in JSON Format
@app.route('/devices.json')
def devices_json():
    response = manager.list_devices()
    response = json.dumps(response)
    return Response(response, 
        mimetype='application/json',
        headers={'Content-Disposition':'attachment;filename=devices.json'})

# Return the Groups in JSON Format
@app.route('/groups.json')
def groups_json():
    response = manager.list_groups()
    response = json.dumps(response)
    return Response(response, 
        mimetype='application/json',
        headers={'Content-Disposition':'attachment;filename=groups.json'})

# Return the dTypes in JSON Format
@app.route('/dtypes.json')
def dtypes_json():
    response = manager.list_dtypes()
    response = json.dumps(response)
    return Response(response, 
        mimetype='application/json',
        headers={'Content-Disposition':'attachment;filename=dtypes.json'})


@app.route('/devices/add', methods=['GET', 'POST'])
def device_add():
    if request.method == 'POST':
        uuid = request.form['uuid']
        dtype = request.form['dtype']
        group = request.form['group']
        new_device = {
            'uuid': uuid,
            'dtype': dtype,
            'group': group
        }
        if not manager.add_device_to_db(new_device):
            flash(u'Invalid uuid', 'error')
        else:
            manager.send_add_message(uuid, dtype)
            flash(u'Device added', 'success')
        return redirect('/devices')
    else:
        next_uuid = len(manager.list_devices())
        return render_template('device_add.html', title='Add New Device', uuid=next_uuid)

@app.route('/devices/<int:device_uuid>')
def device_show(device_uuid):
    device = manager.get_device(device_uuid)
    if not device:
        abort(404)

    return render_template('device_show.html', device=device)

@app.route('/devices/<int:device_uuid>/edit', methods=['GET', 'POST'])
def device_edit(device_uuid):
    device = manager.get_device(device_uuid)
    if not device:
        abort(404)

    if request.method == 'POST':
        uuid = device['uuid']
        dtype = device['dtype']
        group = request.form['group']
        new_device = {
            'uuid': uuid,
            'dtype': dtype,
            'group': group
        }

        manager.remove_device(device_uuid)
        manager.add_device(new_device)
        flash(u'Device updated', 'success')
        return redirect(f'/devices/{device_uuid}')
    else:
        return render_template('device_edit.html', title='Edit Device', device=device)

@app.route('/devices/<int:device_uuid>/<string:command>')
def device_command(device_uuid, command):
    if not command in ["start", "stop", "delete"]:
        abort(404)
    device = manager.get_device(device_uuid)
    if not device:
        abort(404)
    manager.process_device_command(device, command)
    return redirect('/devices')


@app.route('/groups/<int:group_id>/<string:command>')
def group_command(group_id, command):
    if not command in ["start", "stop", "delete"]:
        abort(404)
    groups = manager.list_groups()
    group = groups[group_id]
    for device in group:
        manager.process_device_command(device, command)

    return redirect('/groups')

@app.route('/dtypes/<string:dtype>/<string:command>')
def type_command(dtype, command):
    if not command in ["start", "stop", "delete"]:
        abort(404)
    dtypes = manager.list_dtypes()
    dtype = dtypes[dtype]
    for device in dtype:
        manager.process_device_command(device, command)

    return redirect('/dtypes')

@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404