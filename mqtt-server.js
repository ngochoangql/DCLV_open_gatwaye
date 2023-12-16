// mqtt-server.js
const mosca = require('mosca');
const http = require('http');
const settings = { port: 1883 }; // Cổng MQTT

const server = new mosca.Server(settings);

// Tạo HTTP server để hỗ trợ WebSocket
const httpServer = http.createServer();
httpServer.listen(3000, function () {
  console.log('HTTP server listening on port 3000');
});

server.attachHttpServer(httpServer);

server.on('ready', () => {
  console.log('MQTT Server is ready on port 1883');
});

server.on('clientConnected', (client) => {
  console.log(`Client connected: ${client.id}`);
});

server.on('published', (packet, client) => {
  if (packet.topic !== '$SYS/broker/clients/total') {
    console.log(`Published: ${packet.payload.toString()} to ${packet.topic}`);
  }
});

server.on('subscribed', (topic, client) => {
  console.log(`Subscribed: ${client.id} to ${topic}`);
});

server.on('unsubscribed', (topic, client) => {
  console.log(`Unsubscribed: ${client.id} from ${topic}`);
});

server.on('clientDisconnecting', (client) => {
  console.log(`Client disconnecting: ${client.id}`);
});

server.on('clientDisconnected', (client) => {
  console.log(`Client disconnected: ${client.id}`);
});
