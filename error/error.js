const socket = require("socket.io-client")("http://localhost:3000/error");
const plant = require("socket.io-client")("http://localhost:3000/plant");

const readline = require("readline").createInterface({
  input: process.stdin,
  output: process.stdout
});

let data = { action: 0, type: "" };

socket.on("connect", () => {
  process.stdout.write("Qual o set-point: ");
  readline.on("line", line => {
    const setPointTMP = { action: 0, type: "" };

    if (line.indexOf("ma") !== -1) {
      line = line.replace("ma", "");
      setPointTMP.type = "ma";
    } else {
      setPointTMP.type = "";
    }
    setPointTMP.action = Number(line);

    if (JSON.stringify(setPointTMP) !== JSON.stringify(data)) {
      data = setPointTMP;
    }

    process.stdout.write("Qual o set-point: ");
  });
});

plant.on("read", value => {
  let error = 0;

  if (data.type !== "ma") {
    error = data.action - value;
  } else {
    error = data.action;
  }

  socket.emit("read", { action: error, type: data.type });
});
