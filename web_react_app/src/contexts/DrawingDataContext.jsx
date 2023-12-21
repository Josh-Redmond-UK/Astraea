import React, { createContext, useState, useContext } from 'react';

export const DrawingDataContext = createContext({
    points: null,
    startDate: null,
    endDate: null,
    imageMode: null,
  });