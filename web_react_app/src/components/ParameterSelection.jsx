import React, { useContext, useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPenRuler, faFire, faSeedling, faCamera } from '@fortawesome/free-solid-svg-icons'
import { DrawingDataContext } from '../contexts/DrawingDataContext'
import { UserFlowContext } from '../contexts/UserFlowContext'

const ParameterSelection = ({ onAnalysisComplete }) => {
  const { drawingData, updateDrawingData } = useContext(DrawingDataContext);
  const { step, incrementStep } = useContext(UserFlowContext);
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalysis = async () => {
    setIsLoading(true);
    try {
      let params = JSON.stringify(drawingData);
      let url = "http://127.0.0.1:5000/api";

      // First API call to get the GIF
      const response = await fetch(`${url}/mapping?params=${params}`);
      if (!response.ok) throw new Error('Failed to fetch analysis data');
      const data = await response.json();
  
      

      const gifResponse = await fetch(`${url}/${data.gif_url}`);
      if (!gifResponse.ok) throw new Error('Failed to fetch GIF');
      const gifBlob = await gifResponse.blob();
      const gifUrl = URL.createObjectURL(gifBlob);
  
      // Second API call to get the stats
      const statsResponse = await fetch(`${url}/stats`);
      if (!statsResponse.ok) throw new Error('Failed to fetch stats');
      const statsData = await statsResponse.json();

      // Fetch PNGs
      const pngPromises = data.png_urls.map(async (pngUrl) => {
        console.log(`${url}/${pngUrl}`);
        const pngResponse = await fetch(`${url}/${pngUrl}`);
        if (!pngResponse.ok) throw new Error('Failed to fetch PNG');
        const pngBlob = await pngResponse.blob();
        return URL.createObjectURL(pngBlob);
      });

      const pngUrls = await Promise.all(pngPromises);

      const zipResponse = await fetch(`${url}/${data.zip_url}`);
      if (!zipResponse.ok) throw new Error('Failed to fetch Zip');
      const zipBlob = await zipResponse.blob();
      const zipUrl = URL.createObjectURL(zipBlob);



      // Combine the results and pass them to the parent component
      onAnalysisComplete({
        GifUrl: gifUrl,
        ImgUrls: pngUrls,
        Stats: statsData.Stats,
        ZipUrl: zipUrl
      });
    } catch (error) {
      console.error('Error during analysis:', error);
      // Handle error (e.g., show error message to user)
    } finally {
      setIsLoading(false);
    }
  };


  return (
    <div>
        <h2 className='text-xl'>Select Options</h2>
        Select the options you want to use for your analysis. 
        <br></br>
        <br></br>
        <p className='text-lg'>Date Range</p>
        <div className="join mt-2 w-max">
            <div className='join-item w-1/2 mr-1'>
                <p className='text-center'> Start Date </p>
                <input className='input ' type="date" value={drawingData.start_date} 
                onChange={e => updateDrawingData({start_date:e.target.value})}></input>
            </div>
            <div className='join-item w-1/2 right-1'>
                <p className='text-center'> End Date </p> 
                <input className='input' type="date" value={drawingData.end_date} 
                onChange={e => updateDrawingData({end_date:e.target.value})}></input>
            </div>
        </div>
        <p className='text-lg mt-4'>Image Type</p>
        <select className="select select-bordered w-full max-w-xs" value={drawingData.image_type} 
        onChange={e => updateDrawingData({image_type:e.target.value})}>
        <option disabled selected>Imagery Type</option>
        <option value={"Colour"}>📷 True Colour</option>
        <option value={"NDVI"}>🌳 Vegetation (NDVI)</option>
        <option value={"BAIS2"}>🔥 Burn (BAIS2)</option>
        </select>
        <p className='text-lg mt-4'>Aggregation Type</p>
        <select className="select select-bordered w-full max-w-xs" value={drawingData.agg_type} 
        onChange={e => updateDrawingData({agg_type:e.target.value})}>
        <option disabled selected>Aggregation Type</option>
        <option value={"median"}>Median</option>
        <option value={"mean"}>Mean</option>
        <option value={"max"}>Max Change</option>
        <option value={"none"}>None</option>
        </select>
        <p className='text-lg mt-4'>Aggregation Length</p>
        <select className="select select-bordered w-full max-w-xs" value={drawingData.agg_length} 
        onChange={e => updateDrawingData({agg_length:e.target.value})}>
        <option disabled selected>Aggregation Length</option>
        <option value={"monthly"}>Monthly</option>
        <option value={"annual"}>Annual</option>
        <option value={"none"}>None</option>
        </select>
        <button 
        className={`btn btn-primary w-full mt-4 ${isLoading ? 'loading' : ''}`} 
        onClick={handleAnalysis}
        disabled={isLoading}
      >
        {isLoading ? 'Running Analysis...' : 'Run Analysis'}
      </button>
      <button className="btn btn-primary w-full mt-4" onClick={() => {incrementStep(-1)}}>Go Back</button>
    </div>
  )
}

export default ParameterSelection