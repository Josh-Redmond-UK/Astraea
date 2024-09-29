import React, { useState } from 'react';
import SidebarAlt from './components/SidebarAlt';
import './App.css';
import InteractiveMap from './components/InteractiveMap';
import 'leaflet/dist/leaflet.css';
import { UserFlowContext } from './contexts/UserFlowContext';
import { DrawingContext } from './contexts/DrawingContext';
import { DrawingDataContext } from './contexts/DrawingDataContext';

function App() {
  const [step, setStep] = useState(1);
  const incrementStep = (x) => setStep(step + x);

  const [drawingData, setDrawingData] = useState({
    roi: null,
    start_date: null,
    end_date: null,
    cloud_cover: 100,
    image_type: null,
    agg_type: null,
    agg_length: null
  });

  const updateDrawingData = (newData) => {
    setDrawingData({...drawingData, ...newData})
  };

  const [drawing, setDrawing] = useState(false);
  const toggleDrawing = () => setDrawing(!drawing);

  return (
    <div className="App relative">
      <DrawingDataContext.Provider value={{ drawingData, updateDrawingData }}>
        <DrawingContext.Provider value={{ drawing, toggleDrawing }}>
          <UserFlowContext.Provider value={{ step, incrementStep }}> 

            {/* Sidebar */}
            <div className="absolute top-0 left-0 h-full z-10">
              <SidebarAlt />
            </div>

            {/* Map and Search Options Container */}
            <div className="relative z-0">
              {/* Map Container */}
              <InteractiveMap />
            </div>

          </UserFlowContext.Provider>
        </DrawingContext.Provider>
      </DrawingDataContext.Provider>
    </div>
  );
}

export default App;
