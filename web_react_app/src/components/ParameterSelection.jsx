import React, {useContext} from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPenRuler, faFire, faSeedling, faCamera } from '@fortawesome/free-solid-svg-icons'
import { DrawingDataContext } from '../contexts/DrawingDataContext'
import { UserFlowContext } from '../contexts/UserFlowContext'
const ParameterSelection = () => {

  const { drawingData, updateDrawingData } = useContext(DrawingDataContext);
  const { step, incrementStep } = useContext(UserFlowContext);


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
                <input className='input ' type="date" value={drawingData.endDate} 
                onChange={e => updateDrawingData({startDate:e.target.value})}></input>
            </div>
            <div className='join-item w-1/2 right-1'>
                <p className='text-center'> End Date </p> 
                <input className='input' type="date" value={drawingData.endDate} 
                onChange={e => updateDrawingData({endDate:e.target.value})}></input>
            </div>
        </div>
        <p className='text-lg mt-4'>Image Type</p>
        <select className="select select-bordered w-full max-w-xs" value={drawingData.imageMode} 
        onChange={e => updateDrawingData({imageMode:e.target.value})}>
        <option disabled selected>Imagery Type</option>
        <option value={"true_colour"}>📷 True Colour</option>
        <option> value={"ndvi"}🌳 Vegetation (NDVI)</option>
        <option value={"bais2"}>🔥 Burn (BAIS2)</option>
        </select>
        <p className='text-lg mt-4'>Aggregation Type</p>
        <select className="select select-bordered w-full max-w-xs" value={drawingData.aggType} 
        onChange={e => updateDrawingData({aggType:e.target.value})}>
        <option disabled selected>Aggregation Type</option>
        <option value={"median"}>Median</option>
        <option value={"mean"}>Mean</option>
        <option value={"max"}>Max Change</option>
        <option value={"none"}>None</option>
        </select>
        <p className='text-lg mt-4'>Aggregation Length</p>
        <select className="select select-bordered w-full max-w-xs" value={drawingData.aggLength} 
        onChange={e => updateDrawingData({aggLength:e.target.value})}>
        <option disabled>Aggregation Length</option>
        <option value={"monthly"}>Monthly</option>
        <option value={"annual"}>Annual</option>
        <option value={"none"}>None</option>
        </select>
        <button className="btn btn-primary w-full mt-4" onClick={() => {console.log(drawingData)}}>Run Analysis</button>
        <button className="btn btn-primary w-full mt-4" onClick={() => {incrementStep(-1)}}>Go Back</button>
    </div>
  )
}

export default ParameterSelection