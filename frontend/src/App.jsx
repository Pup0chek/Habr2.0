import React, { useState } from 'react';
import axios from 'axios';
import Results from './Results'; // Изменил 'components.results' на относительный путь './Results'

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);

  const handleSearch = async (event) => {
    event.preventDefault();
    try {
      const graphqlQuery = {
        query: `
          query SearchArticles($q: String!) {
            search(q: $q) {
              id
              title
              content
            }
          }
        `,
        variables: {
          q: query
        }
      };

      // Отправляем POST-запрос на GraphQL endpoint микросервиса gateway
      const response = await axios.post('http://localhost:8000/graphql', graphqlQuery);
      // Предполагается, что ответ имеет структуру: { data: { search: [...] } }
      setResults(response.data.data.search);
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Ошибка при получении результатов поиска');
      setResults([]);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Поиск статей</h1>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Введите поисковый запрос..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ padding: "0.5rem", width: "300px" }}
        />
        <button type="submit" style={{ padding: "0.5rem", marginLeft: "1rem" }}>
          Найти
        </button>
      </form>
      <Results results={results} />
    </div>
  );
}

import { collectDefaultMetrics } from 'prom-client';

// Конфигурация клиентских метрик
const collectMetrics = () => {
  if (typeof window !== 'undefined') { // Проверяем, что код выполняется в браузере
    const client = require('prom-client');
    
    // Сбрасываем предыдущие метрики
    client.register.clear();
    
    // Собираем стандартные метрики
    client.collectDefaultMetrics({
      prefix: 'react_app_',
      gcDurationBuckets: [0.001, 0.01, 0.1, 1, 2, 5], // настройки для сборщика мусора
      register: client.register
    });

    // Отправляем метрики на сервер каждые 10 секунд
    setInterval(() => {
      fetch('http://localhost:4000/metrics', {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain' },
        body: client.register.metrics()
      }).catch(console.error);
    }, 10000);
  }
};

// Инициализация при загрузке приложения
if (typeof window !== 'undefined') {
  collectMetrics();
}

export default App;
