const net = require('net');

var server_port = 65432;
var server_addr = "172.20.68.125";   // the IP address of your Raspberry PI

function client() {
    var input = document.getElementById("myName").value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${input}\r\n`);
    });

    // get the data from the server
    client.on('data', (data) => {
        document.getElementById("greet_from_server").innerHTML = data;
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

function greeting() {

    // get the element from html
    var name = document.getElementById("myName").value;
    // update the content in html
    // document.getElementById("greet").innerHTML = "Hello " + name + " !";
    // send the data to the server 
    client();

}

function send_command(dir, val) {
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        let input = `${dir}:${val}`;
        // console.log(input);
        client.write(`${input}\r\n`);
    });

    // get the data from the server
    client.on('data', (data) => {
        document.getElementById("message-to-server").innerHTML = data;
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


async function update_timestamp() {
    while (true) {
        document.getElementById("timestamp").innerHTML = new Date(Date.now()).toString();
        await sleep(2000);
    }
}