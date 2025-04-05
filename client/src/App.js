import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [repoUrl, setRepoUrl] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/run', { repo_url: repoUrl });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>CLI Runner</h1>
      <form onSubmit={handleSubmit}>
        <label>Enter GitHub Repo URL: </label>
        <input
          type="text"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          required
        />
        <button type="submit">Run</button>
      </form>
      <div id="terminal-placeholder">
        <p>This is where the terminal will go.</p>
      </div>
    </div>
  );
}

export default App;
