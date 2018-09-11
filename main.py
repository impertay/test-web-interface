from flask import Flask
from flask import render_template
from flask import redirect
from flask_socketio import SocketIO

import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

stand_data = {
    'valve': False,
    'pump': False,
    'bottom_capacity': 60,
    'upper_capacity': 40,
    'valve_perc': 0,
}

@app.route('/')
def index():
    return render_template('index.html', title='Заглавная страница', stand_data=stand_data)

@socketio.on('valve_opening', namespace='/flask')
def change_valve_opening(msg):
    global stand_data
    print('msg = ', msg)
    if not stand_data['valve'] and msg == 'open_valve':
        stand_data['valve'] = True
        while stand_data['bottom_capacity'] < 100 and stand_data['valve'] and msg != 'off_pump':
            socketio.sleep(2)
            stand_data['upper_capacity'] -= 2
            stand_data['bottom_capacity'] += 2
            print('Насос в работе и уровень в нижней ёмкости: ', stand_data['bottom_capacity'])
            socketio.emit('filling_bottom_capacity', stand_data, namespace='/flask')

@app.route("/close_valve", methods=['POST'])
def close_valve():
    global stand_data
    stand_data['valve'] = False
    print('Функция close_valve выполнена', stand_data['valve'])
    return redirect('/')

@socketio.on('starting_pump', namespace='/flask')
def pumping(msg):
    global stand_data
    if not stand_data['pump'] and msg == 'on_pump':
        stand_data['pump'] = True
        while stand_data['upper_capacity'] < 100 and stand_data['pump'] and msg != 'off_pump':
            socketio.sleep(2)
            stand_data['upper_capacity'] += 2
            stand_data['bottom_capacity'] -= 2
            print('Насос в работе и уровень в верхней ёмкости: ', stand_data['upper_capacity'])
            socketio.emit('filling_upper_capacity', stand_data, namespace='/flask')
    else:
        print('Насос уже включен', stand_data['pump'])
    print('Функция on_pump выполнена', stand_data['pump'])

@app.route("/off_pump", methods=['POST'])
def off_pump():
    global stand_data
    stand_data['pump'] = False
    print('Функция off_pump выполнена', stand_data['pump'])
    return redirect('/')

if __name__ == '__main__':
    socketio.run(app, debug=True)
