global.mode = "0";

const noble = require("noble");
const dotenv = require("dotenv");
const superagent = require("superagent");
const fs = require("fs");
var d3 = require("d3");
const io = require("socket.io-client");
const type_id = "46";
dotenv.config({ path: "./config.env" });

const MAC = process.env.MAC;
const MAXLOGS = parseInt(process.env.MAXLOGS);
console.log(MAC);
console.log(MAXLOGS);
const socket = io("http://127.0.0.1:5000");
//_________________________________
const possible_mode = ["0", "1", "2"];
socket.on("new_mode", (msg) => {
  if (msg.mac == MAC) {
    if (possible_mode.includes(msg.mode)) {
      global.mode = msg.mode;
      console.log(global.mode);
    }
  }
});

socket.on("syncronize", (msg) => {
  /*if (msg.mac == MAC) {
    functions.syncronizeSensor(global.sensors, MAC);
  }*/
});
socket.on("desconnect", (reason) => {
  console.log(`reason: ${reason}`);
});
socket.on("connect", () => {
  console.log("connected");

  socket.emit("newrspi", MAC);

  setTimeout(() => {
    //after logging wait 3 second, in this 3 second those lines can't be executed (if->line 28), after this timeout those lines can be executed (cond=true)

    console.log("3 sec passati");
    functions.syncronizeSensor(global.sensors, MAC);
    functions.syncronizeLogs(global.logs, MAC);
  }, 3000);
});

socket.open();

//________________________________________________
//________________________________________________

const functions = require("./functions");
//___________________________________________
global.sensors = JSON.parse(
  fs.readFileSync("./components/capture.json", "utf-8")
);
console.log(global.sensors);

var ids = global.sensors.map((el) => {
  //array with all ids
  return el.DEVICE_ID;
});
//____________________________________
global.logs = JSON.parse(fs.readFileSync("./components/logs.json", "utf-8"));

//console.log(ids);

//____________________________
//salvare localmente stato allarme e insieme di sensori

var cond = true;

noble.on("scanStart", () => {
  console.log("start");
});

noble.on("discover", (state) => {
  try {
    if (state.advertisement.manufacturerData) {
      const piece = state.advertisement.manufacturerData.toString("hex");
      const Adv = functions.nobleAdvParser(piece);
      const initAdv = functions.initAdvParser(piece);
      const payload = { id: Adv.DEVICE_ID };

      if (cond && Adv.TYPE_ID == type_id) {
        data = { mac: MAC };

        if (global.mode == "1") {
          console.log("INIT");

          superagent
            .post("http://localhost:5000/sensor/check")
            .set("accept", "json")
            .send(payload)
            .then((res) => {
              console.log("--------------------ONLINE-----------------");
              console.log(res.text);
              if (res.text == "not exist") {
                functions.newSensor(
                  Adv.DEVICE_ID,
                  Adv.TYPE_ID,
                  MAC,
                  Adv.FIRMWARE_VERSION
                );
              }
              console.log("--------------------OFFLINE-----------------");

              if (!ids.includes(initAdv.DEVICE_ID)) {
                //ALSO OFFLINE

                console.log("id not exist");
                global.sensors.push(initAdv);
                fs.writeFile(
                  "./components/capture.json",
                  JSON.stringify(global.sensors),
                  (err) => {
                    if (err) console.log;
                    console.log("create new sensor in json");
                  }
                );
                ids.push(initAdv.DEVICE_ID);
              } else {
                console.log("id exist");
              }
            })
            .catch((err) => {
              //offline case
              console.log("--------------------OFFLINE-----------------");

              console.log(`err: ${err.errno}`);
              if (ids.includes(initAdv.DEVICE_ID)) {
                console.log("id exist");
              } else {
                console.log("id not exist");
                global.sensors.push(initAdv);
                fs.writeFile(
                  "./components/capture.json",
                  JSON.stringify(global.sensors),
                  (err) => {
                    if (err) console.log;
                    console.log("create new sensor in json");
                  }
                );
                ids.push(initAdv.DEVICE_ID);
              }
            });
        } else if (global.mode != "1") {
          console.log("ALARM");
          superagent
            .post("http://localhost:5000/sensor/check")
            .set("accept", "json")
            .send(payload)
            .then((res) => {
              console.log("--------------------ONLINE-----------------");

              console.log(res.text);
              if (res.text == "exist") {
                //global.sensors.push(initAdv);

                console.log(Adv.DEVICE_ID, " : ", piece, " : ", Adv.EVENT_DATA);

                functions.alarm(Adv.DEVICE_ID, Adv.EVENT_DATA);
              }
              console.log("--------------------OFFLINE-----------------");

              if (ids.includes(Adv.DEVICE_ID)) {
                /*global.sensors = global.sensors.map((el) => {
                  if (Adv.DEVICE_ID == el.DEVICE_ID) {
                    el.EVENT_DATA = Adv.EVENT_DATA;
                  }
                  return el;
                });
                fs.writeFile(
                  './components/capture.json',
                  JSON.stringify(global.sensors),
                  (err) => {
                    if (err) console.log;
                    console.log('file writed');
                  }
                );*/
                const counter = functions.howMany(global.logs, Adv.DEVICE_ID);
                console.log(counter);
                if (counter >= MAXLOGS) {
                  console.log("fuori limite");
                  var where = global.logs
                    .map((el) => el.deviceID)
                    .indexOf(Adv.DEVICE_ID);
                  global.logs.splice(where, 1);
                }
                global.logs.push({
                  deviceID: Adv.DEVICE_ID,
                  event: Adv.EVENT_DATA,
                  whenEvent: Date().toString(),
                });
                fs.writeFile(
                  "./components/logs.json",
                  JSON.stringify(global.logs),
                  (err) => {
                    if (err) console.log;
                    console.log("file writed");
                  }
                );
              }
            })
            .catch((err) => {
              //ofline mode
              console.log("--------------------OFFLINE-----------------");

              if (err.errno == "ECONNREFUSED") {
                if (ids.includes(Adv.DEVICE_ID)) {
                  const counter = functions.howMany(global.logs, Adv.DEVICE_ID);
                  console.log(counter);
                  if (counter >= MAXLOGS) {
                    console.log("fuori limite");
                    var where = global.logs
                      .map((el) => el.deviceID)
                      .indexOf(Adv.DEVICE_ID);
                    global.logs.splice(where, 1);
                  }
                  global.logs.push({
                    deviceID: Adv.DEVICE_ID,
                    event: Adv.EVENT_DATA,
                    whenEvent: Date().toString(),
                  });
                  fs.writeFile(
                    "./components/logs.json",
                    JSON.stringify(global.logs),
                    (err) => {
                      if (err) console.log;
                      console.log("file writed");
                    }
                  );
                }
              }
            });
        }

        cond = false;
        setTimeout(() => {
          //after logging wait 3 second, in this 3 second those lines can't be executed (if->line 28), after this timeout those lines can be executed (cond=true)
          cond = true;
        }, 1000 * process.env.TIMEOUT);
      }
    }
  } catch (Err) {
    console.log(Err);
  }
});

noble.startScanning([], true, () => {});
