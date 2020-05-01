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
    return render_template('devices.html', devices=response )

# Return the Groups in HTML Format
@app.route('/groups')
def groups():
    response = manager.list_groups()
    return render_template('groups.html', groups=response )

# Return the Devices in JSON Format
@app.route('/devices.json')
def devices_json():
    response = manager.list_devices()
    return jsonify(response)

# Return the Groups in JSON Format
@app.route('/groups.json')
def groups_json():
    response = manager.list_groups()
    return jsonify(response)

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
        if manager.add_device(new_device):
            flash(u'Device added', 'success')
        else:
            flash(u'Invalid uuid', 'error')

        return redirect('/devices')
    else:
        next_uuid = len(manager.list_devices())
        return render_template('device_add.html', title='Add New Device', uuid=next_uuid)


@app.route('/devices/<int:device_uuid>/delete')
def device_delete(device_uuid):
    device = manager.get_device(device_uuid)
    if not device:
        abort(404)
    manager.remove_device(device_uuid)
    
    return redirect('/devices')


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


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404