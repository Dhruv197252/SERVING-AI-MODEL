import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [text, setText] = useState("");

  const [result, setResult] = useState(null);

  const [task, setTask] = useState("sentiment");

  const [loading, setLoading] = useState(false);



  async function handleSubmit() {

    setLoading(true);

    const response = await axios.post(

      `http://127.0.0.1:8000/${task}`,

      {
        text: text
      }

    );

    setResult(response.data);

    setLoading(false);

  }



  return (

    <div className="container">

      <h1>AI NLP Playground</h1>



      {/* Select Task */}

      <select

        value={task}

        onChange={(e) => setTask(e.target.value)}

      >

        <option value="sentiment">

          Sentiment Analysis

        </option>

        <option value="generate">

          Text Generation

        </option>

        <option value="ner">

          Named Entity Recognition

        </option>

      </select>




      {/* Input */}

      <textarea

        placeholder="Enter text..."

        value={text}

        onChange={(e) => setText(e.target.value)}

      />




      {/* Button */}

      <button onClick={handleSubmit}>

        {

          loading

            ? "Loading..."

            : "Submit"

        }

      </button>




      {/* Output */}

      <div className="output">

        <h2>Result</h2>

        {

          result && (

            <pre>

              {JSON.stringify(result, null, 2)}

            </pre>

          )

        }

      </div>

    </div>

  );

}

export default App;