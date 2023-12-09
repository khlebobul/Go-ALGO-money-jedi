async function getSimpleExplanation() {
  const scientificInput = document.getElementById('scientificInput').value;

  // Replace 'YOUR_API_KEY' with your OpenAI API key
  const apiKey = 'YOUR_API_KEY';

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
          document.getElementById('simpleExplanation').innerText = simpleExplanation;
      } else {
          throw new Error('Invalid response format from OpenAI API');
      }
  } catch (error) {
      console.error('Error:', error.message);
      // Handle the error, e.g., display a user-friendly message on the page
  }
}