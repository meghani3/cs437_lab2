const net = require('net');

var server_port = 1030;
var server_addr = "192.168.0.107";   // the IP address of your Raspberry PI

function request_server(input, ele) {
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log(`sending :${input} to server`);
        client.write(`${input}\r\n`);
    });

    // get the data from the server
    client.on('data', (data) => {
        document.getElementById(ele).innerHTML = data.toString().split('\n').join("<br>");
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

function send_command(dir, val) {
    let input = `${dir}:${val}`;
    let ele = "message-to-server";
    request_server(input, ele)
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


async function update_timestamp() {
    while (true) {
        // document.getElementById("timestamp").innerHTML = new Date(Date.now()).toString();
        request_server("stats", "timestamp")
        await sleep(2000);
    }
}