const express = require('express');
const http = require('http');
require('dotenv').config();

const routes = require('./routes/routes');

const app = express();
const server = http.createServer(app);

app.use(express.json());
app.use('/', routes);

const PORT = 3800;
server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});