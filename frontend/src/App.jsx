import { useEffect, useState } from "react";
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

  const [documents, setDocuments] = useState([]);
  const [documentsLoading, setDocumentsLoading] = useState(false);
  const [documentsMessage, setDocumentsMessage] = useState("");

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [rewrittenQuery, setRewrittenQuery] = useState("");
  const [asking, setAsking] = useState(false);

  const loadDocuments = async () => {
    setDocumentsLoading(true);
    setDocumentsMessage("");

    try {
      const token = localStorage.getItem("access_token");

      const response = await fetch(
        "http://127.0.0.1:8001/documents",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to load documents");
      }

      setDocuments(data);
    } catch (error) {
      setDocumentsMessage(error.message);
    } finally {
      setDocumentsLoading(false);
    }
  };

  useEffect(() => {
    if (loggedIn) {
      loadDocuments();
    }
  }, [loggedIn]);

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

      setUploadMessage(`Upload successful: ${data.filename}`);
      setSelectedFile(null);

      const fileInput = document.getElementById("document-upload");

      if (fileInput) {
        fileInput.value = "";
      }

      await loadDocuments();
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
    setSelectedFile(null);
    setUploadMessage("");
    setRewrittenQuery("");
    setDocuments([]);
  };

  if (loggedIn) {
    return (
      <div className="dashboard">

        <header className="dashboard-header">
          <div>
            <h1>Enterprise Knowledge</h1>
            <p>Knowledge Intelligence Platform</p>
          </div>

          <button onClick={handleLogout}>
            Logout
          </button>
        </header>

        <main className="dashboard-content">

          <h2>Knowledge Dashboard</h2>

          <p>
            Manage documents and interact with your enterprise knowledge.
          </p>

          {/* Upload */}

          <section className="upload-section">

            <h3>📄 Upload Document</h3>

            <p>
              Upload a PDF to add it to your enterprise knowledge base.
            </p>

            <input
              id="document-upload"
              type="file"
              accept=".pdf,application/pdf"
              onChange={(event) => {
                setSelectedFile(event.target.files[0] || null);
                setUploadMessage("");
              }}
            />

            {selectedFile && (
              <p>
                Selected file: <strong>{selectedFile.name}</strong>
              </p>
            )}

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

          </section>

          {/* Documents */}

          <section className="documents-section">

            <div className="documents-header">

              <div>
                <h3>📚 My Documents</h3>

                <p>
                  Documents available in your knowledge base.
                </p>
              </div>

              <button
                onClick={loadDocuments}
                disabled={documentsLoading}
              >
                {documentsLoading ? "Refreshing..." : "Refresh"}
              </button>

            </div>

            {documentsMessage && (
              <p className="message">
                {documentsMessage}
              </p>
            )}

            {!documentsLoading && documents.length === 0 && !documentsMessage && (
              <div className="empty-documents">
                <p>No documents uploaded yet.</p>
              </div>
            )}

            {documents.length > 0 && (
              <div className="document-list">

                {documents.map((document) => (
                  <div
                    className="document-item"
                    key={document.id}
                  >

                    <div className="document-icon">
                      📄
                    </div>

                    <div className="document-info">

                      <strong>
                        {document.filename}
                      </strong>

                      <span>
                        Document ID: {document.id}
                      </span>

                      <span>
                        Status: {document.status}
                      </span>

                    </div>

                    <div className="document-status">
                      {document.status}
                    </div>

                  </div>
                ))}

              </div>
            )}

          </section>

          {/* AI Assistant */}

          <section className="assistant-section">

            <h3>🤖 AI Knowledge Assistant</h3>

            <p>
              Ask questions about information contained in your uploaded
              enterprise documents.
            </p>

            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Example: What is this document about?"
              rows="4"
            />

            <button
              onClick={handleAsk}
              disabled={asking || !question.trim()}
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

                    <strong>
                      Rewritten query:
                    </strong>

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

                      Hybrid:{" "}
                      {typeof source.score === "number"
                        ? source.score.toFixed(3)
                        : "N/A"}

                      {" | "}

                      Semantic:{" "}
                      {typeof source.semantic_score === "number"
                        ? source.semantic_score.toFixed(3)
                        : "N/A"}

                      {" | "}

                      Keyword:{" "}
                      {typeof source.keyword_score === "number"
                        ? source.keyword_score.toFixed(3)
                        : "N/A"}

                      {" | "}

                      Rerank:{" "}
                      {typeof source.rerank_score === "number"
                        ? source.rerank_score.toFixed(3)
                        : "N/A"}

                    </small>

                  </div>
                ))}

              </div>
            )}

          </section>

          {/* Feature Cards */}

          <div className="dashboard-cards">

            <div className="dashboard-card">
              <h3>📄 Documents</h3>
              <p>
                Upload and manage organizational documents.
              </p>
            </div>

            <div className="dashboard-card">
              <h3>🔎 Knowledge Search</h3>
              <p>
                Search information across your enterprise documents using
                semantic and keyword retrieval.
              </p>
            </div>

            <div className="dashboard-card">
              <h3>🤖 AI Assistant</h3>
              <p>
                Get answers grounded in retrieved document content with
                source information.
              </p>
            </div>

          </div>

        </main>
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

            <p>
              Knowledge Intelligence Platform
            </p>
          </div>

        </div>

        <div className="login-header">

          <h2>Welcome back</h2>

          <p>
            Sign in to access your organization's knowledge.
          </p>

        </div>

        <form onSubmit={handleLogin}>

          <label htmlFor="email">
            Email
          </label>

          <input
            id="email"
            type="email"
            placeholder="you@company.com"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
            required
          />

          <label htmlFor="password">
            Password
          </label>

          <input
            id="password"
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