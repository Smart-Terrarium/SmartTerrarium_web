
var socket = new WebSocket('ws://localhost:8000/data')

socket.onmessage = function (e){
    var djangoData = JSON.parse(e.data);
    console.log(djangoData);

    document.querySelector('#app').innerHTML = djangoData;
}