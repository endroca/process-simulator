const http = require("http").createServer();
const io = require("socket.io")(http);

/**
 * Namespace Error
 */
const error = io.of("/error");
error.on("connection", client => {
  console.log("Client error added");

  client.on("read", value => {
    error.emit("read", value);
  });
});

/**
 * Namespace Controller
 */
const controller = io.of("/controller");
controller.on("connection", client => {
  console.log("Client controller added");

  client.on("read", value => {
    controller.emit("read", value);
  });
});

/**
 * Namespace Plant
 */
const plant = io.of("/plant");
plant.on("connection", client => {
  console.log("Client plant added");

  client.on("read", value => {
    plant.emit("read", value);
  });
});

http.listen(3000);
