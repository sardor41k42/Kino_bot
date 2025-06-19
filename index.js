const TelegramBot = require('node-telegram-bot-api');
const config = require('./config.json');
const https = require('https');
// ... kod davom ettiriladi (sizlik yuborgan matn)

getGenreList();

function getGenreList() {
  fetchJSONFile(genreListAPI)
    .then((data) => {
      genreList = data;
    })
    .catch((err) => console.error(err));
}