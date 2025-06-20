const TelegramBot = require('node-telegram-bot-api');
const https = require('https');

const config = {
  tokenBot: '7485332977:AAEK79wCat0v0_6zim08bH6gV9wpy54ZIc0',
  keyAPI: '45c0b71bc1e828a09e9879172ff307ea'
};

const bot = new TelegramBot(config.tokenBot, { polling: true });

const escapeHTML = (str) =>
  str.replace(/&/g, "&amp;")
     .replace(/</g, "&lt;")
     .replace(/>/g, "&gt;")
     .replace(/"/g, "&quot;")
     .replace(/'/g, "&#039;");

function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (err) {
          reject(err);
        }
      });
    }).on('error', reject);
  });
}

function formatMovies(results) {
  if (!results || results.length === 0) return "🎬 Kino topilmadi.";
  const movie = results[0];
  const title = escapeHTML(movie.title || "Noma'lum");
  const rating = movie.vote_average || "Noma'lum";
  const date = movie.release_date || "Noma'lum";
  const overview = escapeHTML(movie.overview || "Tavsif yo'q.");
  const link = `https://www.themoviedb.org/movie/${movie.id}?language=ru`;
  const poster = movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : null;

  let msg = `<b>${title}</b>

`;
  msg += `<b>Reyting:</b> ${rating}/10
`;
  msg += `<b>Chiqqan sana:</b> ${date}

`;
  msg += `${overview}

`;
  msg += `<a href="${link}">🔗 TMDB'da ko‘rish</a>`;
  return { msg, poster };
}

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, `🎬 Salom ${msg.from.first_name || "do‘st"}!

Buyruqlar:
/search <kino nomi>
/upcoming - Yaqinda chiqadigan kinolar`, {
    parse_mode: "HTML"
  });
});

bot.onText(/\/search (.+)/, async (msg, match) => {
  const chatId = msg.chat.id;
  const query = encodeURIComponent(match[1]);
  const url = `https://api.themoviedb.org/3/search/movie?query=${query}&language=ru&api_key=${config.keyAPI}`;

  try {
    const data = await fetchJSON(url);
    const result = formatMovies(data.results);
    if (result.poster) {
      bot.sendPhoto(chatId, result.poster, { caption: result.msg, parse_mode: "HTML" });
    } else {
      bot.sendMessage(chatId, result.msg, { parse_mode: "HTML" });
    }
  } catch (err) {
    console.error("Xatolik:", err.message);
    bot.sendMessage(chatId, "❌ Kino topishda xatolik yuz berdi.");
  }
});
