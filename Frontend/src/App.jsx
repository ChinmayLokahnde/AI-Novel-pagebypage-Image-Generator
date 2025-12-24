import { useState } from "react";

function App() {
  const [image, setImage] = useState(null);
  const [data, setData] = useState(null);

  const generateImage = async () => {
    const res = await fetch("http://127.0.0.1:8000/image/generate/1", {
      method: "POST",
    });

    const json = await res.json();
    setData(json);

    if (json.image) {
      setImage(`data:image/png;base64,${json.image}`);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>AI Book Visualizer</h1>

      <button 
        onClick={generateImage}
        style={{ padding:"10px 20px", marginBottom: "20px" }}>
        Generate Page Image
      </button>
      {image && (
        <div>
          <h2>Generated Illustration</h2>
          <img src={image} alt="Generated" width="400" />
        </div>
      )}
      {data && (
        <div style={{ marginTop: "20px" }}>
          <h2>Page Metadata</h2>
          <pre>{JSON.stringify(data.analysis, null, 2)}</pre>

          <h3>AI Prompt Used:</h3>
<div style={{ background:"#eee", padding:"10px", borderRadius:"5px" }}>
  <p><strong>Main Prompt:</strong> {data.prompt.prompt}</p>
  <p><strong>Negative Prompt:</strong> {data.prompt.negative_prompt}</p>
</div>
        </div>
      )}
    </div>
  );
}

export default App;
