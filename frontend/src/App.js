import React, { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first!");

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze-resume", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      console.error(err);
      alert("Backend not responding.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>AI Resume Analyzer</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <br />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>

      {response && (
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <h3>Analysis Result:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
