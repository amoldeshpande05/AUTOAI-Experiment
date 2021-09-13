const express = require('express')
var path = require('path');
const app = express()
const port = 8080
app.get('/', (req, res) => {
  let jsonPath = path.join(__dirname, 'index.html');
  res.sendFile(jsonPath);
})

app.listen(port, (req,res) => {
  console.log("Listening on the port  : ",port)
})


app.use(express.static(__dirname));
