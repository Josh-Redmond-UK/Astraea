import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const AnalysisResults = ({ data, onBack }) => {
  const { ImgUrls, GifUrl, Stats } = data;

  // Prepare data for the chart
  const chartData = Stats.map((stat, index) => ({
    date: stat.image_path.split('/').pop().split('.')[0], // Extract date from filename
    ...stat.band_stats.reduce((acc, band, i) => {
      acc[`Band ${i+1}`] = band.mean;
      return acc;
    }, {})
  }));

  return (
    <div className="analysis-results p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Analysis Results</h2>
        <button
          onClick={onBack}
          className="btn btn-primary"
        >
          Back to Map
        </button>
      </div>
      
      <div className="mb-6">
        <h3 className="text-xl font-semibold mb-2">Animated GIF</h3>
        <img src={GifUrl} alt="Analysis GIF" className="w-full max-w-2xl mx-auto" />
      </div>

      <div className="mb-6">
        <h3 className="text-xl font-semibold mb-2">Statistics Timeline</h3>
        <div className="w-full max-w-4xl mx-auto">
          <LineChart width={800} height={400} data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            {Object.keys(chartData[0]).filter(key => key !== 'date').map((key, index) => (
              <Line key={key} type="monotone" dataKey={key} stroke={`#${Math.floor(Math.random()*16777215).toString(16)}`} />
            ))}
          </LineChart>
        </div>
      </div>

      <div>
        <h3 className="text-xl font-semibold mb-2">Individual Images</h3>
        <div class="carousel rounded-box">
          {ImgUrls.map((url, index) => (
            <div class="carousel-item"><img key={index} src={url} alt={`Analysis Image ${index + 1}`} className="w-full" /></div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults;