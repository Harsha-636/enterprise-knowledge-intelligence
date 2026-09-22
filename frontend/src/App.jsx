import { useState } from "react";
import "./App.css";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploading, setUploading] = useState(false);

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [rewrittenQuery, setRewrittenQuery] = useState("");
  const [asking, setAsking] = useState(false);

  const handleLogin = async (event) => {
    event.preventDefault();

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8001/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email,
            password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

      localStorage.setItem("access_token", data.access_token);
      setLoggedIn(true);

    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadMessage("Please select a PDF first.");
      return;
    }

    setUploading(true);
    setUploadMessage("");

    try {
      const token = localStorage.getItem("access_token");

      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(
        "http://127.0.0.1:8001/documents/upload",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setUploadMessage(
        `Upload successful: ${data.filename}`
      );

      setSelectedFile(null);

    } catch (error) {
      setUploadMessage(error.message);
    } finally {
      setUploading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) {
      return;
    }

    setAsking(true);
    setAnswer("");
    setSources([]);
    setRewrittenQuery("");

    try {
      const token = localStorage.getItem("access_token");

      const response = await fetch(
        "http://127.0.0.1:8001/rag/query",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            question: question,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Question failed");
      }

      setAnswer(data.answer);
      setSources(data.sources || []);
      setRewrittenQuery(data.rewritten_query || "");

    } catch (error) {
      setAnswer(error.message);
    } finally {
      setAsking(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setLoggedIn(false);
    setAnswer("");
    setSources([]);
    setQuestion("");
  };

  if (loggedIn) {
    return (
      <div className="dashboard">

        <div className="dashboard-header">

          <div>
            <h1>Enterprise Knowledge</h1>
            <p>Knowledge Intelligence Platform</p>
          </div>

          <button onClick={handleLogout}>
            Logout
          </button>

        </div>

        <div className="dashboard-content">

          <h2>Knowledge Dashboard</h2>

          <p>
            Manage documents and interact with your enterprise knowledge.
          </p>

          <div className="upload-section">

            <h3>📄 Upload Document</h3>

            <p>
              Upload a PDF to add it to the knowledge base.
            </p>

            <input
              type="file"
              accept=".pdf"
              onChange={(event) =>
                setSelectedFile(event.target.files[0])
              }
            />

            <button
              onClick={handleUpload}
              disabled={uploading}
            >
              {uploading ? "Uploading..." : "Upload PDF"}
            </button>

            {uploadMessage && (
              <p className="upload-message">
                {uploadMessage}
              </p>
            )}

          </div>

          <div className="assistant-section">

            <h3>🤖 AI Knowledge Assistant</h3>

            <p>
              Ask a question about your uploaded documents.
            </p>

            <textarea
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              placeholder="Example: What programming skills does Harsha have?"
              rows="4"
            />

            <button
              onClick={handleAsk}
              disabled={asking}
            >
              {asking ? "Thinking..." : "Ask AI"}
            </button>

            {answer && (
              <div className="answer-box">

                <h4>Answer</h4>

                <p className="answer">
                  {answer}
                </p>

                {rewrittenQuery && (
                  <div className="query-info">
                    <strong>Rewritten query:</strong>
                    <br />
                    {rewrittenQuery}
                  </div>
                )}

              </div>
            )}

            {sources.length > 0 && (
              <div className="sources-box">

                <h4>Sources</h4>

                {sources.map((source) => (
                  <div
                    className="source"
                    key={source.chunk_id}
                  >

                    <strong>
                      Chunk {source.chunk_id}
                    </strong>

                    <p>
                      {source.content}
                    </p>

                    <small>
                      Hybrid: {source.score.toFixed(3)}
                      {" | "}
                      Rerank: {source.rerank_score.toFixed(3)}
                    </small>

                  </div>
                ))}

              </div>
            )}

          </div>

          <div className="dashboard-cards">

            <div className="dashboard-card">
              <h3>📄 Documents</h3>
              <p>
                Upload and manage your organizational documents.
              </p>
            </div>

            <div className="dashboard-card">
              <h3>🔎 Knowledge Search</h3>
              <p>
                Search information across your documents.
              </p>
            </div>

            <div className="dashboard-card">
              <h3>🤖 AI Assistant</h3>
              <p>
                Get grounded answers with document citations.
              </p>
            </div>

          </div>

        </div>

      </div>
    );
  }

  return (
    <div className="app">

      <div className="login-card">

        <div className="brand">

          <div className="logo">
            EK
          </div>

          <div>
            <h1>Enterprise Knowledge</h1>
            <p>Knowledge Intelligence Platform</p>
          </div>

        </div>

        <div className="login-header">

          <h2>Welcome back</h2>

          <p>
            Sign in to access your organization's knowledge.
          </p>

        </div>

        <form onSubmit={handleLogin}>

          <label>Email</label>

          <input
            type="email"
            placeholder="you@company.com"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
            required
          />

          <label>Password</label>

          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            required
          />

          <button
            type="submit"
            disabled={loading}
          >
            {loading ? "Signing in..." : "Sign in"}
          </button>

        </form>

        {message && (
          <p className="message">
            {message}
          </p>
        )}

        <div className="login-footer">
          Secure enterprise knowledge access
        </div>

      </div>

    </div>
  );
}

export default App;