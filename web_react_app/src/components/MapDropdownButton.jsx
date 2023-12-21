import React, { useState } from 'react';

const MapDropdownButton = () => {
    const [showDropdown, setShowDropdown] = useState(false);

    const toggleDropdown = () => setShowDropdown(!showDropdown);

    return (
        <div className="absolute top-10 left-10 z-50">
            <button onClick={toggleDropdown} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Menu
            </button>
            {showDropdown && (
                <div className="mt-2 py-2 w-48 bg-white rounded-lg shadow-xl">
                    <a href="#" className="block px-4 py-2 text-gray-800 hover:bg-gray-200">Menu Item 1</a>
                    <a href="#" className="block px-4 py-2 text-gray-800 hover:bg-gray-200">Menu Item 2</a>
                    {/* Add more menu items as needed */}
                </div>
            )}
        </div>
    );
};

export default MapDropdownButton;
