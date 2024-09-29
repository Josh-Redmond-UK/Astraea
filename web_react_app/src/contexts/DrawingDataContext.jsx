import React, { createContext, useState, useContext } from 'react';

export const DrawingDataContext = createContext({
    points: null,
    start_date: null,
    end_date: null,
    image_type: null,
    agg_length:null,
    agg_type:null,

  });