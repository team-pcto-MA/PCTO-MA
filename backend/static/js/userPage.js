url = new URL(window.location.href);
const vett = url.pathname.split('/');
const user = vett[2];
const card = $('#rspi').text();

//_______________________________________________________________________________

const sensors = async (mac) => {
  if (mac) {
    try {
      const Res = await fetch(`${url.origin}/sensor?mac=${mac}`);
      const res = await Res.json();
      console.log(res);
      let sensors = [];
      if (res.status != '200') {
        alert(`Error: ${res.status} : ${res.message}`);
      } else {
        if (res.data.length == 0) {
          $('#logs').append('<h2>This RSPI has no sensor</h2>');
        } else {
          let c = 0;
          res.data.forEach((el) => {
            console.log(el.dev_id);
            $('#sensors').append(
              `<div class="" id="sensor${c}">${el.dev_id}</div>`
            );
            sensors.push($(`#sensor${c}`));
            c += 1;
          });
          console.log(sensors);
          sensors.forEach((el) => {
            el.click(() => {
              $('#logs').empty();

              el.siblings().attr('class', '');
              el.attr('class', 'active_2');

              const id_s = el.text();

              fetch(`${url.origin}/log/sensorLogs`, {
                method: 'POST',
                body: JSON.stringify({ id_s: id_s }),
              })
                .then((log) => log.json())
                .then((Log) => {
                  console.log(Log);
                  if (Log.status != '200') {
                    alert(`Error, ${Log.status}: ${Log.message}`);
                  } else {
                    if (Log.data.length == 0) {
                      $('#logs').append('<h2>This sensor have no logs</h2>');
                    } else {
                      Log.data.forEach((log) => {
                        console.log('ciao');
                        $('#logs').append(
                          `<h3>Event: ${log.event}.  When: ${log.whenEvent}</h3>`
                        );
                      });
                    }
                  }
                })
                .catch((er) => {
                  console.log(er);
                });
            });
          });
        }
      }
    } catch (err) {
      console.log(`Error: ${err}`);
    }
  }
};

const togglePopup = (mac) => {
  console.log(mac);
  var popup = document.getElementById('popup');
  popup.classList.toggle('active');
  $('#logs').empty();

  $('#sensors').empty();
  sensors(mac);
};

$(document).ready(async () => {
  console.log('ready');
  console.log(url);
  console.log(vett);
  console.log(card);
  $('#contenitore').append(card);
});

//_______________________________________________________________________________
$('#logout').click(async () => {
  console.log('ciao');
  const rowRes = await fetch(`/user/logOut`);
  const res = await rowRes.json();

  if (res.status == '200') {
    console.log(res.status);
    window.location.href = 'login';
  }
});
//_______________________________________________________________________________
$('#add').click(async () => {
  window.location.href = `${url.origin}/view/${user}/rspreg`;
});

$('#rspiList').click(() => {});

[$('#rspiList'), $('#userInfo'), $('#add'), $('#logout')].forEach((el) => {
  el.click(() => {
    $('#contenitore').empty();
    if (el.attr('id') == 'rspiList') {
      console.log(card);
      $('#contenitore').append(card);
    }
    el.attr('class', 'active');
    el.siblings().attr('class', '');
  });
});

$('#userInfo').click(async () => {
  Res = await fetch(`${url.origin}/user`);
  res = await Res.json();
  if (res.status != '200') {
    alert(`Error : ${res.status}: ${res.message}`);
  } else {
  }
});
