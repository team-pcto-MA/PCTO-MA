//10c2352746012499
//PER FARE UNA PROVA : 02010609086953656E736F722009FF10C23527460343BA
const dict = {
  '00': 'NORMAL',
  '01': 'TAMPER',
  '02': 'ALARM',
  '03': 'ALARM,TAMPER',
  '04': 'BATTERY',
  '05': 'BATTERY,TAMPER',
  '06': 'BATTERY,ALARM',
  '07': 'BATTERY,ALARM,TAMPER',
  '08': 'HEARTBEAT',
  '09': 'HEARTBEAT,TAMPER',
  '0A': 'HEARTBEAT,ALARM',
  '0B': 'HEARTBEAT,ALARM,TAMPER',
  '0C': 'HEARTBEAT,BATTERY',
  '0D': 'HEARTBEAT,BATTERY,TAMPER',
  '0E': 'HEARTBEAT,BATTERY,ALARM',
  '0F': 'HEARTBEAT,BATTERY,ALARM,TAMPER',
};
exports.advParser = (adv) => {
  let adv_data = [];
  const Adv = {
    AD_LENGHT: '',
    AD_TYPE: '',
    MFG_ID: '',
    NOTHING_1: '',
    NOTHING_2: '',
    i: '',
    S: '',
    e: '',
    n: '',
    s: '',
    o: '',
    r: '',
    DEVICE_NAME_TERMINATOR: '',
    DATA_LEGHT_SENSOR: '',
    SENSOR_DATA_BIT: '',
    FIRMWARE_VERSION: '',
    DEVICE_ID: '',
    TYPE_ID: '',
    EVENT_DATA: '',
    CONTROL_DATA: '',
    NOTHING_3: '',
  };

  //console.log(stringa.slice(1, 3));
  for (let a = 0; a < adv.length; a += 2) {
    adv_data.push(adv.slice(a, a + 2));
  }

  let cont = 0;
  for (const key in Adv) {
    if (key != 'DEVICE_ID' && key != 'EVENT_DATA') {
      Adv[key] = adv_data[cont];
      cont += 1;
    } else if (key == 'EVENT_DATA') {
      Adv[key] = dict[adv_data[cont]];
      cont += 1;
    } else {
      Adv[key] = adv_data[cont] + adv_data[cont + 1] + adv_data[cont + 2];
      cont += 3;
    }
  }

  return Adv;
};

exports.syncronizeLogs = async (logs, mac) => {
  console.log('inizio sincro');

  try {
    const superagent = require('superagent');
    payload = { logs: logs, mac: mac };
    console.log(payload);
    const res = await superagent
      .post('http://localhost:5000/log/syncronize')
      .set('accept', 'json')
      .send(payload);

    console.log(res.text);
  } catch (err) {
    console.log(`err : ${err}`);
  }
};

exports.howMany = (objList, id) => {
  let counter = 0;
  for (obj of objList) {
    if (obj.deviceID == id) {
      counter += 1;
    }
  }
  return counter;
};

exports.syncronizeSensor = async (sensors, mac) => {
  console.log('inizio sincro');

  try {
    const superagent = require('superagent');
    payload = { sensors: sensors, mac: mac };
    console.log(payload);
    const res = await superagent
      .post('http://localhost:5000/sensor/syncronize')
      .set('accept', 'json')
      .send(payload);

    console.log(res.text);
  } catch (err) {
    console.log(`err : ${err}`);
  }
};

exports.nobleAdvParser = (slice) => {
  const Adv = {
    FIRMWARE_VERSION: '',
    DEVICE_ID: '',
    TYPE_ID: '',
    EVENT_DATA: '',
  };
  let adv_data = [];

  for (let a = 0; a < slice.length; a += 2) {
    adv_data.push(slice.slice(a, a + 2));
  }
  let cont = 0;
  for (const key in Adv) {
    if (key != 'DEVICE_ID') {
      Adv[key] = adv_data[cont];
      cont += 1;
    } else {
      Adv[key] = adv_data[cont] + adv_data[cont + 1] + adv_data[cont + 2];
      cont += 3;
    }
  }

  return Adv;
};
exports.initAdvParser = (slice) => {
  const Adv = {
    FIRMWARE_VERSION: '',
    DEVICE_ID: '',
    TYPE_ID: '',
  };
  let adv_data = [];

  for (let a = 0; a < slice.length; a += 2) {
    adv_data.push(slice.slice(a, a + 2));
  }
  let cont = 0;
  for (const key in Adv) {
    if (key != 'DEVICE_ID') {
      Adv[key] = adv_data[cont];
      cont += 1;
    } else {
      Adv[key] = adv_data[cont] + adv_data[cont + 1] + adv_data[cont + 2];
      cont += 3;
    }
  }

  return Adv;
};

exports.findByDeviceId = (vett, id) => {
  var cond = false;
  for (a in vett) {
    if (a.DEVICE_ID === id) {
      cond = true;
      break;
    }
  }
  return cond;
};

exports.pause = (ms) => {
  let now = new Date().getTime();
  let fine = now + ms;

  while (now < fine) {
    now = new Date().getTime();
  }
};

exports.alarm = async (id, event) => {
  const superagent = require('superagent');

  try {
    const query = `id=${id}&event=${event}&date=${Date().toString()}`;
    const res = await superagent
      .get('http://localhost:5000/log/insertLog')
      .query(query);

    console.log(res.text);
  } catch (err) {
    console.log('err: ', err);
  }
};

exports.newSensor = async (id, type_id, mac_RSPi, firm_ver) => {
  const superagent = require('superagent');

  try {
    //const query = `id=${id}&type_id=${type_id}&mac=${mac_RSPi}&firm_ver=${firm_ver}&event=${event}`;

    const data = {
      id: id,
      type_id: type_id,
      mac: mac_RSPi,
      firm_ver: firm_ver,
    };

    const res = await superagent
      .post('http://localhost:5000/sensor')
      .set('accept', 'json')
      .send(data);

    console.log(res.text);
  } catch (err) {
    console.log('err: ', err);
  }
};

//console.log(this.nobleAdvParser('10c2352746012499'));
//console.log(this.advParser('02010609086953656E736F722009FF10c2352746012499'));
