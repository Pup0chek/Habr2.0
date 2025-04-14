import React, { useState } from 'react';

function Add_topic({ topic_title, tags, data, author }) {
  const [error, setError] = useState(null);

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <h2>Результаты:</h2>
      {results.length > 0 ? (
        <ul>
          {results.map((item) => (
            <li key={item.id}>
              <h3>{item.title}</h3>
              <p>{item.content}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>Нет результатов</p>
      )}
    </div>
  );
}

export default Results;
