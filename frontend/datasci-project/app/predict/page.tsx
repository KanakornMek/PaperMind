// app/predict.tsx
"use client";
import React, { useState } from "react";

const Predict: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [text, setText] = useState("");
  const [results, setResults] = useState<{
    subjectArea: string;
    confidence: number;
  } | null>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = event.target.files?.[0] || null;
    //read text from file
    const reader = new FileReader();
    reader.onload = (e) => {
      if (e.target) {
        setText(e.target.result as string);
      }
    };
    if (uploadedFile) {
      reader.readAsText(uploadedFile);
    }
    setFile(uploadedFile);
  };

  const handleTextChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: JSON.stringify({ text: text }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setResults({
          subjectArea: data.predicted_label,
          confidence: data.probabilities[data.predicted_label],
      });
      console.log(data);
    } catch (error) {
        //print error http code
        console.error("Error:", error);
        
    }
    // const mockResult = {
    //   subjectArea: "Computer Science",
    //   confidence: 0.95,
    // };
    // setResults(mockResult);
  };

  return (
    <section className="bg-gray-100 py-12 h-full overflow-auto">
      <div className="container mx-auto px-6">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Predict the Subject Area
        </h2>
        <p className="text-center text-gray-600 mb-12">
          Upload your research paper or paste your text to get AI-powered
          predictions.
        </p>
        <div className="flex flex-col md:flex-row justify-between items-start">
          <div className="w-full md:w-2/3 mb-8 md:mb-0">
            <div className="mb-4">
              <label
                className="block text-gray-700 font-semibold mb-2"
                htmlFor="fileUpload"
              >
                Upload your text file
              </label>
              <input
                type="file"
                id="fileUpload"
                onChange={handleFileUpload}
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>
            <div className="mb-4">
              <label
                className="block text-gray-700 font-semibold mb-2"
                htmlFor="textUpload"
              >
                Or paste your text
              </label>
              <textarea
                id="textUpload"
                rows={6}
                value={text}
                onChange={handleTextChange}
                className="w-full p-2 border border-gray-300 rounded text-gray-800 h-40"
                placeholder="Paste your text here"
              />
            </div>
            <button
              onClick={handleSubmit}
              className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
            >
              Predict
            </button>
            {results && (
              <div className="mt-8">
                <h3 className="text-xl font-semibold text-gray-800">
                  Prediction Results:
                </h3>
                <p className="text-gray-700 mt-2">
                  <strong>Subject Area:</strong> {results.subjectArea}
                </p>
                <p className="text-gray-700 mt-2">
                  <strong>Confidence:</strong>{" "}
                  {(results.confidence).toFixed(2)}%
                </p>
              </div>
            )}
          </div>
          <div className="w-full md:w-1/3 md:pl-8">
            <div className="bg-white p-6 shadow-md rounded-lg">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">
                Tips for better predictions
              </h3>
              <ul className="list-disc list-inside text-gray-600">
                <li>Ensure your text is clear and well-structured.</li>
                <li>Upload files in supported formats (e.g., txt).</li>
                <li>Include relevant keywords and phrases.</li>
              </ul>
            </div>
            <div className="bg-white p-6 shadow-md rounded-lg mt-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">
                Examples of subject areas
              </h3>
              <ul className="list-disc list-inside text-gray-600">
                <li>Medicine</li>
                <li>Computer Science</li>
                <li>Mathematics</li>
                <li>Engineering</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Predict;
