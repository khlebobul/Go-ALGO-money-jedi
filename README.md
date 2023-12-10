# [Хакатон GO ALGO ]([url](https://goalgo.ru/)https://goalgo.ru/) | Команда Денежные джедаи

### Идея проекта

На основании данных MOEXALGO API наше решение будет "предсказывать" тренд (направление движения)
определенной валютной пары / актива на несколько дней вперед, основываясь на данных последних X дней и
экономических новостях, которые могут повлиять на цену и волатильность данной валютной
пары / актива.

Данный сервис создан для людей, у которых уже есть опыт в торговле. Целевая аудитория - начинающие и опытные трейдеры.
Цель сервиса - помочь трейдеру принять решение о покупке/продаже конкретного актива на бирже, путем предоставления ему спрогнозированных цен закрытия и новостей по отслеживаемым активам.

### Какие данные использованы
- MOEXALGO API
- Financial News Sentiment Dataset (FiNeS)
- Standard Candles

### Usage [Explain Like I'm Five](https://www.reddit.com/r/explainlikeimfive/)

```javascript

// Replace 'YOUR_API_KEY' with your OpenAI API key
  const apiKey = 'YOUR_API_KEY';

```
