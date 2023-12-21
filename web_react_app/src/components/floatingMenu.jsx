import React, { useState } from 'react';

const FloatingMenu = () => {


  return (
    <details className="dropdown relative">
          <summary className="btn focus:btn-primary">Search</summary>
          <div className="bg-white shadow-md p-2 rounded-md mt-2 absolute -translate-x-96">
            <h2 className="text-lg">Enter Coordinates</h2>
            <div className="join">
                <input type="text" placeholder="Latitude" className="input input-bordered  join-item" />
                <input type="text" placeholder="Longitude" className="input input-bordered  join-item" />
                <button className="btn btn-primary join-item">Go</button>
            </div>
            <div className="divider"></div>
            <h2 className="text-lg">Search Location</h2>
            <div className="join w-full">
                <input type="text" placeholder="Enter Location Name" className="input input-bordered w-full join-item" />
                <button className="btn btn-primary join-item">Go</button>
            </div>

          </div>
          </details>


  );
};

export default FloatingMenu;
