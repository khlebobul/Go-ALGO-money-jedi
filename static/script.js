const companyItems = document.querySelectorAll(".company__list__item");
const translatorButton = document.querySelector(".translator__window__button");
const closeTranslator = document.querySelector(".translator__window__close");
const companies = document.querySelectorAll(".company__list__item");
const newsList = document.querySelector(".center__news__list");
let chosenElemnt = companyItems[0];




const newsItem = (title, sentimental, url)=>{
  return`
  <a href="${url}"  class="center__news__list__item">
                        
                        <div class="center__news__list__item__left">
                        <div class="center__news__list__item__left__text">
                            <span class="center__news__list__item__left__text__bold">${title}</span>
                        </div>
                        </div>
                        <span class="center__news__list__item__indicator">${sentimental}</span>
                    </a>
  `
}

const fadeIn = (el, timeout, display) =>{
  el.style.opacity = 0;
  el.style.display = display || 'flex';
  el.style.transition = `opacity ${timeout}ms`
  setTimeout(() => {
      el.style.opacity = 1;
  }, 10);
};

const fadeOut = (el, timeout) =>{
  el.style.opacity = 1;
  el.style.transition = `opacity ${timeout}ms`
  el.style.opacity = 0;

  setTimeout(() => {
      el.style.display = 'none';
  },timeout);
};


chosenElemnt.classList.add("active");
companyItems.forEach(item => {
    item.addEventListener("click", function(){
        item.classList.add("active");
        item.style.transition = "all 1s";
        chosenElemnt.classList.remove("active");
        chosenElemnt = item;
    })
});


async function getSimpleExplanation() {
  const scientificInput = document.querySelector(".translator__window__textarea").value;


  // Replace 'YOUR_API_KEY' with your OpenAI API key
  const apiKey = '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';

  try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${apiKey}`,
          },
          body: JSON.stringify({
              model: 'gpt-3.5-turbo',
              messages: [
                  { role: 'system', content: 'You are a helpful assistant.' },
                  { role: 'user', content: scientificInput },
              ],
            max_tokens: 500,
          }),
      });

      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      if (data.choices && data.choices.length > 0 && data.choices[0].message && data.choices[0].message.content) {
          const simpleExplanation = data.choices[0].message.content;
          document.querySelector(".translator__window__translated-text").innerText = simpleExplanation;
      } else {
          throw new Error('Invalid response format from OpenAI API');
      }
  } catch (error) {
      console.error('Error:', error.message);
      // Handle the error, e.g., display a user-friendly message on the page
  }
}

async function getNews(tiker){
    const response = await fetch("http://http://127.0.0.1:8000/api/news/" + ticker);
    let resp = response.json();
}

document.querySelector(".translator-open").addEventListener("click", function(){
  fadeIn(document.querySelector(".translator"), 1000);
});

closeTranslator.addEventListener("click", function(){
    fadeOut(document.querySelector(".translator"), 1000);
});

translatorButton.addEventListener("click", getSimpleExplanation);



// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.0.0/firebase-app.js";
import { getDatabase, ref, set, child, get } from 'https://www.gstatic.com/firebasejs/10.0.0/firebase-database.js';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyA9aleV8-ynwRI_wAI9jGtsSEVxFersp2k",
  authDomain: "goalgo-1170e.firebaseapp.com",
  databaseUrl: "https://goalgo-1170e-default-rtdb.firebaseio.com/",
  projectId: "goalgo-1170e",
  storageBucket: "goalgo-1170e.appspot.com",
  messagingSenderId: "401039936016",
  appId: "1:401039936016:web:1900dbbc161ab0b3761895"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);


get(child(ref(database), 'news/')).then((snapshot) => {
  if (snapshot.exists()) {
  } else {
      console.log("No data available");
  }
}).catch((error) => {
      console.error(error);
});

document.addEventListener("DOMContentLoaded", function(){
  get(child(ref(database), 'news/GAZP')).then((snapshot) => {
    if (snapshot.exists()) {
        snapshot.val().title.forEach((e, i) => {
          let title = e.toString();
          let sentimental = snapshot.val().sentiment[i] > 0 ? "✅" : "❌";
          let url = snapshot.val().source[i];
          newsList.insertAdjacentHTML("beforeend", newsItem(title, sentimental, url));
        });
    } else {
        console.log("No data available");
    }
  }).catch((error) => {
        console.error(error);
  });
});

const ctx = document.getElementById('myChartGAZP');

const genericOptions = {
  fill: false,
  interaction: {
    intersect: false
  },
  radius: 0,
};
const skipped = (ctx, value) => ctx.p0.skip || ctx.p1.skip ? value : undefined;
const down = (ctx, value) => ctx.p0.parsed.y > ctx.p1.parsed.y ? value : undefined;
const labels = [];
const datas = [];

companies.forEach(el => {
  el.addEventListener("click", function() {
    let oldNews = document.querySelectorAll(".center__news__list__item");
    oldNews.forEach(e => {
      e.remove();
    })
    getNews(el.id);
    get(child(ref(database), 'news/' + el.id.toString())).then((snapshot) => {
      if (snapshot.exists()) {
          snapshot.val().title.forEach((e, i) => {
            let title = e.toString();
            let sentimental = snapshot.val().sentiment[i] > 0 ? "✅" : "❌";
            let url = snapshot.val().source[i];
            newsList.insertAdjacentHTML("beforeend", newsItem(title, sentimental, url));
          });
      } else {
          console.log("No data available");
      }
    }).catch((error) => {
          console.error(error);
    });
    document.querySelectorAll(".item").forEach(e => {
      e.style.display = 'none';
    })
    document.getElementById('myChart'+el.id).style.display = 'block';
    const ctx = document.getElementById('myChart'+el.id);

    const genericOptions = {
      fill: false,
      interaction: {
        intersect: false
      },
      radius: 0,
    };
    const skipped = (ctx, value) => ctx.p0.skip || ctx.p1.skip ? value : undefined;
    const down = (ctx, value) => ctx.p0.parsed.y > ctx.p1.parsed.y ? value : undefined;
    const labels = [];
    const datas = [];
get(child(ref(database), '/сhart/' + el.id)).then((snapshot) => {
    if (snapshot.exists()) {
      
        snapshot.val().timestamp.forEach((e, i) => {
          labels.push(e.toString());
          datas.push(snapshot.val().amount[i]);
        });
        const data = {
          labels: labels,
          datasets: [{
            label: 'Текущая цена',
            data: datas,
            borderColor: 'rgb(75, 192, 192)',
            segment: {
              borderColor: ctx => skipped(ctx, 'rgb(0,0,0,0.2)') || down(ctx, 'rgb(192,75,75)'),
              borderDash: ctx => skipped(ctx, [6, 9]),
            },
            spanGaps: true
          }]
        };
        const config = {
          type: 'line',
          data: data,
          options: genericOptions
        };
        
        const myChart = new Chart(ctx, config);
    } else {
        console.log("No data available");
    }
  }).catch((error) => {
        console.error(error);
  });
  })
})


get(child(ref(database), '/сhart/GAZP')).then((snapshot) => {
    if (snapshot.exists()) {
        snapshot.val().timestamp.forEach((e, i) => {
          labels.push(e.toString());
          datas.push(snapshot.val().amount[i]);
        });
        const data = {
          labels: labels,
          datasets: [{
            label: 'Текущая цена',
            data: datas,
            borderColor: 'rgb(75, 192, 192)',
            segment: {
              borderColor: ctx => skipped(ctx, 'rgb(0,0,0,0.2)') || down(ctx, 'rgb(192,75,75)'),
              borderDash: ctx => skipped(ctx, [6, 9]),
            },
            spanGaps: true
          }]
        };
        const config = {
          type: 'line',
          data: data,
          options: genericOptions
        };
        
        const myChart = new Chart(ctx, config);
    } else {
        console.log("No data available");
    }
  }).catch((error) => {
        console.error(error);
  });





