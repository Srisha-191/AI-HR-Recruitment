import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Use environment variable if set, else default to localhost:8000
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a resume file first!");
      return;
    }

    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    if (!allowedTypes.includes(file.type)) {
      alert("Only PDF and DOCX files are allowed!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(`${API_URL}/analyze-resume`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const message = await res.text();
        throw new Error(`Server ${res.status}: ${message}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Error:", err);
      alert("❌ Unable to connect to backend. Make sure FastAPI is running on http://localhost:8000");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>AI Resume Analyzer</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit" style={{ marginLeft: "10px" }}>
          {loading ? "Analyzing..." : "Upload & Analyze"}
        </button>
      </form>

      {loading && <p>⏳ Please wait... analyzing your resume.</p>}

      {result && (
        <div
          style={{
            marginTop: "20px",
            padding: "15px",
            border: "1px solid #ccc",
            borderRadius: "5px",
          }}
        >
          <h2>Analysis Result</h2>
          <p><strong>Score:</strong> {result.score}</p>
          <p><strong>Skills:</strong> {Array.isArray(result.skills) ? result.skills.join(", ") : "N/A"}</p>
          <p><strong>Preview:</strong> {result.preview || "No preview available."}</p>
        </div>
      )}
    </div>
  );
}

export default App;
