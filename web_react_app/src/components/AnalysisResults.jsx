import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const AnalysisResults = ({ data, onBack }) => {
  const { ImgUrls, GifUrl, Stats, ZipUrl } = data;
  const ZipData = {'zip_url': ZipUrl, 'filename':'analysis_results.zip'};

  // Prepare data for the chart
  const chartData = Stats.map((stat, index) => ({
    date: stat.image_path.split('/').pop().split('.')[0], // Extract date from filename
    ...stat.band_stats.reduce((acc, band, i) => {
      acc[`Band ${i+1}`] = band.mean;
      return acc;
    }, {})
  }));

  return (
    <div className="analysis-results container mx-auto px-[5%]">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-4xl font-bold pt-5">Analysis Results</h1>
      </div>

      <div className="mb-6">
        <h3 className="text-xl font-semibold mb-2">Animated GIF</h3>
        <img src={GifUrl} alt="Analysis GIF" className="w-full max-w-2xl mx-auto" />
      </div>
      <div class="divider"></div>

      <div className="mb-6">
        <h3 className="text-xl font-semibold mb-2">Statistics Timeline</h3>
        <div className="w-full max-w-4xl mx-auto">
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              {Object.keys(chartData[0]).filter(key => key !== 'date').map((key, index) => (
                <Line key={key} type="monotone" dataKey={key} stroke={`#${Math.floor(Math.random()*16777215).toString(16)}`} />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div class="divider"></div>

      <div>
        <h3 className="text-xl font-semibold mb-2">Individual Images</h3>
        <div className="carousel rounded-box">
          {ImgUrls.map((url, index) => (
            <div key={index} className="carousel-item">
              <img src={url} alt={`Analysis Image ${index + 1}`} className="w-full" />
            </div>
          ))}
        </div>
        <div class="divider"></div>
        <div class="join">

        <a
          className="btn btn-primary join-item"
          href={ZipData.zip_url}
          download={ZipData.filename}
        >
          Download Zip File
        </a>

        <button
          onClick={onBack}
          className="btn btn-primary join-item"
        >
          Back to Map
        </button>
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults;