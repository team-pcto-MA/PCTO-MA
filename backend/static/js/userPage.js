url = new URL(window.location.href);
const vett = url.pathname.split('/');
const user = vett[2];
const card = $('#rspi').text();

//_______________________________________________________________________________

const sensors = async () => {};

$(document).ready(async () => {
  console.log('ready');
  console.log(url);
  console.log(vett);

  const res = await fetch(`${url.origin}/RSPi?user=${user}`);
  const resj = await res.json();
  console.log(resj);
  if (resj.status != '200') {
    alert(`errore: ${resj.message}`);
  } else {
    const data = resj.data;
    console.log(data);

    for (rspi of data) {
      $('#contenitore').append(
        card.replace('%mac%', rspi.name ? rspi.name : rspi.mac)
      );
    }
  }

  const child = $('#s_list').children();
  /*  
  child.each((idx, el) => {
    el.click(() => {
      el.attr('class', 'active');
      el.siblings().attr('class', '');
    });
  });
  */
});
const togglePopup = (mac) => {
  console.log(mac);
  var popup = document.getElementById('popup');
  popup.classList.toggle('active');
};
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

$('#rspiList').click(async () => {
  const res = await fetch(`${url.origin}/RSPi?user=${user}`);
  const resj = await res.json();
  console.log(resj);
  if (resj.status != '200') {
    alert(`errore: ${resj.message}`);
  } else {
    const data = resj.data;
    console.log(data);

    for (rspi of data) {
      $('#contenitore').append(
        card.replace('%mac%', rspi.name ? rspi.name : rspi.mac)
      );
    }
  }
});

[$('#rspiList'), $('#userInfo'), $('#add'), $('#logout')].forEach((el) => {
  el.click(() => {
    $('#contenitore').empty();

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
