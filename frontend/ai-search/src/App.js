import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = async () => {
        try {
            const response = await axios.get(`http://localhost:8000/search`, {
                params: { query, top_k: 5 }
            });
            setResults(response.data);
        } catch (error) {
            console.error("Error searching:", error);
        }
    };

    return (
        <div>
            <h1>AI Search Engine</h1>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter search query"
            />
            <button onClick={handleSearch}>Search</button>
            <ul>
                {results.map((result) => (
                    <li key={result.id}>{result.id} - Score: {result.score}</li>
                ))}
            </ul>
        </div>
    );
}

export default App;
