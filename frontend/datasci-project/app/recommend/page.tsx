"use client";

import React, { useState } from 'react';
import Layout from '../layout';

const Recommend: React.FC = () => {
  const [text, setText] = useState('');
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTextChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(event.target.value);
  };

  const handleSubmit = async () => {
    if (!text.trim()) {
      setError('Please paste your research text.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:8000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input_text: text,
          top_k: 5, 
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch recommendations.');
      }

      const data = await response.json();
      setRecommendations(data);
    } catch (err) {
      setError('Error fetching recommendations. Please try again later.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
      <section className="bg-gray-100 py-12 h-full overflow-auto">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Research Paper Recommendation</h2>
          <p className="text-center text-gray-600 mb-12">
            Paste your research text below to receive AI-powered recommendations for related research papers.
          </p>
          <div className="flex flex-col md:flex-row justify-between items-start">
            <div className="w-full md:w-2/3 mb-8 md:mb-0">
              <div className="mb-4">
                <label className="block text-gray-700 font-semibold mb-2" htmlFor="textInput">
                  Paste your research text
                </label>
                <textarea
                  id="textInput"
                  rows={6}
                  value={text}
                  onChange={handleTextChange}
                  className="w-full p-2 border border-gray-300 rounded"
                  placeholder="Paste your research text here"
                />
              </div>
              <button
                onClick={handleSubmit}
                className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
              >
                {loading ? 'Loading...' : 'Get Recommendations'}
              </button>
              {error && <p className="text-red-500 mt-4">{error}</p>}
              {recommendations.length > 0 && (
                <div className="mt-8">
                  <h3 className="text-xl font-semibold text-gray-800">Recommended Papers:</h3>
                  <ul className="list-disc list-inside text-gray-700 mt-4">
                    {recommendations.map((paper: any, index) => (
                      <li key={index} className="mt-2">
                        <strong>{paper.title}</strong>: {paper.abstract}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>
  );
};

export default Recommend;
