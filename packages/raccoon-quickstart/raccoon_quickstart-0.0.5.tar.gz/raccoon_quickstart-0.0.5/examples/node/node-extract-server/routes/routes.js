const express = require('express');

const raccoonController = require('../controllers/raccoonController');

const router = express.Router();

router.post('/lam/run', raccoonController.runRaccoonAPI);

module.exports = router;