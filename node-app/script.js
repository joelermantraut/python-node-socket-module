const Socket = require(`${__dirname}/Socket.js`);

const SERVER = 1;
const PORT = 3000;

var socketIO = new Socket(
    "localhost",
    PORT,
    SERVER,
    ["name1", "name2"],
    on_read_callback
);

function on_read_callback(msg, namespace) {
    console.log(msg, namespace);

    socketIO.send_message("message from name1", "name1");
}

function main() {
}

main()
