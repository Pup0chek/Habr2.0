import React, { useState } from 'react';
import axios from 'axios';
import Results from './components/results';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [documentTitle, setDocumentTitle] = useState('');
  const [content, setContent] = useState('');
  const [author, setAuthor] = useState('');

  const handleSearch = async (event) => {
    event.preventDefault();
    try {
      const graphqlQuery = {
        query: `
          query Search($q: String!) {
            search(q: $q) {
              id
              title
              content
              author
            }
          }
        `,
        variables: {
          q: query
        }
      };

      const response = await axios.post('http://localhost:8000/graphql', graphqlQuery);
      setResults(response.data.data.search);
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Ошибка при получении результатов поиска');
      setResults([]);
    }
  };

  const createDocument = async (event) => {
    event.preventDefault();
    try {
      const graphqlMutation = {
        query: `
          mutation CreateDocument($title: String!, $content: String!, $author: String) {
            createDocument(title: $title, content: $content, author: $author) {
              id
              title
              content
              author
            }
          }
        `,
        variables: {
          title: documentTitle,
          content: content,
          author: author || null
        }
      };

      const response = await axios.post('http://localhost:8000/graphql', graphqlMutation);
      
      if (response.data.errors) {
        throw new Error(response.data.errors[0].message);
      }

      setError(null);
      alert('Документ успешно создан!');
      // Очищаем форму после успешного создания
      setDocumentTitle('');
      setContent('');
      setAuthor('');
    } catch (err) {
      console.error(err);
      setError('Ошибка при создании документа: ' + err.message);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Добавить документ</h1>
      <form onSubmit={createDocument}>
        <input
          type="text"
          placeholder="Введите название документа"
          value={documentTitle}
          onChange={(e) => setDocumentTitle(e.target.value)}
          style={{ padding: "0.5rem", width: "300px", display: "block", marginBottom: "0.5rem" }}
          required
        />
        <textarea
          placeholder="Введите содержание документа"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          style={{ padding: "0.5rem", width: "300px", display: "block", marginBottom: "0.5rem", minHeight: "100px" }}
          required
        />
        <input
          type="text"
          placeholder="Введите автора (необязательно)"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          style={{ padding: "0.5rem", width: "300px", display: "block", marginBottom: "0.5rem" }}
        />
        <button type="submit" style={{ padding: "0.5rem" }}>
          Создать документ
        </button>
      </form>

      <h1>Поиск документов</h1>
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

      {error && <div style={{ color: "red", margin: "1rem 0" }}>{error}</div>}
      <Results results={results} />
    </div>
  );
}

export default App;