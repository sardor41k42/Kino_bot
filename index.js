const TelegramBot = require('node-telegram-bot-api');
const https = require('https');

const config = {
  tokenBot: process.env.BOT_TOKEN,
  keyAPI: process.env.KEY_API
};

const token = config.tokenBot;
const bot = new TelegramBot(token, { polling: true });

const upcomingAPI = "https://api.themoviedb.org/3/movie/upcoming?language=ru&api_key=" + config.keyAPI;

const fetchJSONFile = function(url) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? require('https') : require('http');
    const request = lib.get(url, (response) => {
      if (response.statusCode < 200 || response.statusCode > 299) {
         reject(new Error('Failed to load page, status code: ' + response.statusCode));
       }
      const body = [];
      response.on('data', (chunk) => body.push(chunk));
      response.on('end', () => resolve(JSON.parse(body.join(''))));
    });
    request.on('error', (err) => reject(err));
  });
};

function getMovies(data) {
  let answer = "";
  data.results.slice(0, 5).forEach((movie, index) => {
    answer += `<b>${index + 1}.</b> <a href='https://www.themoviedb.org/movie/${movie.id}?language=ru'>${movie.title}</a>
<b>Рейтинг:</b> ${movie.vote_average}/10 (${movie.vote_count})
<b>Дата выхода:</b> ${movie.release_date}

`;
  });
  return answer;
}

bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, `Salom ${msg.from.first_name || "do‘st"}! 🎬\n\nBuyruqlar:\n/upcoming - Yaqinda chiqadigan kinolar`, {
    parse_mode: "HTML"
  });
});

bot.onText(/\/upcoming/, (msg) => {
  const chatId = msg.chat.id;
  fetchJSONFile(upcomingAPI)
    .then((data) => {
      bot.sendMessage(chatId, getMovies(data), {parse_mode : "HTML"});
    })
    .catch((err) => {
      bot.sendMessage(chatId, "Xatolik yuz berdi. Keyinroq urinib ko‘ring.");
      console.error(err);
    });
});