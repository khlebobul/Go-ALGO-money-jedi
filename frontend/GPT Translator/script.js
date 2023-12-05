function translate() {
    const apiKey = 'YOUR_API_KEY'; // Replace with your own API key
    const englishText = document.getElementById('englishText').value;
    const targetLanguage = 'ru'; // Russian language code
  
    const url = `https://translation.googleapis.com/language/translate/v2?key=${apiKey}`;
    const data = {
      q: englishText,
      target: targetLanguage
    };
  
    fetch(url, {
      method: 'POST',
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
      const translatedText = result.data.translations[0].translatedText;
      document.getElementById('translatedText').innerText = translatedText;
    })
    .catch(error => console.error('Error:', error));
  }
  