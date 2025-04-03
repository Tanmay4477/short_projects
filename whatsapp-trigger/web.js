const { Client } = require('whatsapp-web.js');
const axios = require('axios');
const qrcode = require('qrcode-terminal');

const client = new Client();
const aiResponseUrl = "http://localhost:8000/";
let lastQRLog = 0;

const sendResponse = async (msg) => {
    try {
        const response = await axios.post(aiResponseUrl, {
            input: msg
        }, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        return("Bhai 2 min ruk, reply krta hu abhi")
    }
};

client.on('qr', (qr) => {
    const now = Date.now();
    if ((now - lastQRLog) > 60000) {
        console.log("it reaches here");
        console.log(qrcode.generate(qr, {small: true}));
        console.log("it also reaches here");
        lastQRLog = now;
    }
});

client.on('ready', () => {
    console.log('Client is ready!');
});

client.on('message', async (msg) => {
    if (msg.body) {
        console.log(msg.body, "yeh to message h");
        const response = await sendResponse(msg.body);
        msg.reply(response)
    }
});

client.initialize();
