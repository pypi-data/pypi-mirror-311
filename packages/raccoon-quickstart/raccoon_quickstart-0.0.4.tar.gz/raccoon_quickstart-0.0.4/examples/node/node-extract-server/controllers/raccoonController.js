const axios = require("axios");
const dotenv = require("dotenv");
const { Readable } = require("stream");

dotenv.config();

const runRaccoonAPI = async (req, res) => {
    try {
        const raccoonPasscode = req.headers["raccoon-passcode"] || "";
        const secretKey = process.env.RACCOON_SECRET_KEY;

        if (!raccoonPasscode) {
            return res.status(400).json({ error: "Missing 'raccoon-passcode' header." });
        }

        const requestBody = req.body;
        console.log(requestBody)
        const stream = requestBody.stream || false;

        const raccoonResponse = await axios.post(
            "https://fitting-wildly-owl.ngrok-free.app/lam/run",
            requestBody,
            {
                headers: {
                    "Content-Type": "application/json",
                    "raccoon-passcode": raccoonPasscode,
                    "secret-key": secretKey,
                },
                responseType: stream ? "stream" : "json",
            }
        );

        if (stream) {
            const readableStream = new Readable({
                read() {
                    raccoonResponse.data.on("data", (chunk) => {
                        this.push(chunk);
                    });

                    raccoonResponse.data.on("end", () => {
                        this.push(null);
                    });
                },
            });

            res.setHeader("Content-Type", "application/json");
            readableStream.pipe(res);
        } else {
            res.status(raccoonResponse.status).json(raccoonResponse.data);
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Internal Server Error" });
    }
};

module.exports = {
    runRaccoonAPI,
};
