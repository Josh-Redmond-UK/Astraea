import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPenRuler, faUpload} from '@fortawesome/free-solid-svg-icons'
import { UserFlowContext } from '../contexts/UserFlowContext'
import { useContext } from 'react'
import { DrawingContext } from '../contexts/DrawingContext'

const DrawControl = () => {
  const {step, incrementStep} = useContext(UserFlowContext);
  const {drawing, toggleDrawing} = useContext(DrawingContext)

  return (
    <div>
            <h2 className='text-lg'>Draw Polygon</h2>
            <br></br>
            <button className="btn btn-accent w-full" onClick={() => {toggleDrawing()}}>Draw<FontAwesomeIcon icon={faPenRuler} /></button>
            <br></br>
            <br></br>
            Draw a polygon on the map to select the area you want to analyse. Press the button above to begin.
            <div className="divider">OR</div>
            <h2 className='text-lg'>Upload Geometry</h2>
            <br></br>
            <button className="btn btn-accent w-full">Upload <FontAwesomeIcon icon={faUpload}/> </button>
            <br></br>
            <br></br>
            If you have a geometry file of the area you want to analyse, you can upload it here instead of drawing a polygon.
            <div className="divider">THEN</div>
            <div className='w-full'>
                <br></br>
                <br></br>
                <button className=" btn btn-primary w-full">Reset</button>
            </div>

    </div>
  )
}

export default DrawControl