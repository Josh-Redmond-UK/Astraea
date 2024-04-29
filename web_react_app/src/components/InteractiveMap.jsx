import React, { useContext, useEffect, useRef } from 'react';
import "leaflet/dist/leaflet.css";
import 'leaflet-draw/dist/leaflet.draw.css';
import Control from 'react-leaflet-custom-control';
import { EditControl } from "react-leaflet-draw";
import { MapWidget } from '../widgets/LeafletMapWidget.js';
import { DrawingContext } from '../contexts/DrawingContext.jsx';
import { UserFlowContext } from '../contexts/UserFlowContext.jsx';
import { DrawingDataContext } from '../contexts/DrawingDataContext.jsx';

const InteractiveMap = () => {
  const { drawing, toggleDrawing } = useContext(DrawingContext);
  const { step, incrementStep } = useContext(UserFlowContext);
  const { drawingData, updateDrawingData } = useContext(DrawingDataContext);
  const containerRef = useRef(null);
  const mapRef = useRef(null);

  useEffect(() => {
    if (!mapRef.current) {
      mapRef.current = new MapWidget(containerRef.current);
      mapRef.current.setZoom(6);
    }

    const handleDrawing = async () => {
      if (drawing) {
        try {
          const drawnPoints = await mapRef.current.startDraw();
          updateDrawingData({ roi: drawnPoints });
          
          toggleDrawing(); // Toggle drawing state
          incrementStep(1); // Increment step in user flow
          console.log(drawingData);
        } catch (error) {
          console.error("Error during drawing:", error);
        }
      } else {
        mapRef.current.stopDraw();
      }
    };

    handleDrawing();
  }, [drawing, drawingData, updateDrawingData]); // Dependency: 'drawing' state

  return (
    <div ref={containerRef} className='map-container' />
  );
};

export default InteractiveMap;
