import React, { useContext } from 'react';
import SearchOptions from './SearchOptions';
import DrawControl from './DrawControl';
import ParameterSelection from './ParameterSelection';
import { UserFlowContext } from '../contexts/UserFlowContext';

const SidebarAlt = ({ onAnalysisComplete }) => {
    const {step, incrementStep} = useContext(UserFlowContext);
    return (
        <div className="drawer lg:drawer-open">
            <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />
            <div className="drawer-content flex flex-col items-center justify-center">
                <label htmlFor="my-drawer-2" className="btn btn-primary drawer-button lg:hidden mt-10">Show Options</label>
            </div> 
            <div className="drawer-side">
                <label htmlFor="my-drawer-2" aria-label="close sidebar" className="drawer-overlay"></label> 
                <ul className="menu p-4 w-80 min-h-full bg-base-200 text-base-content">
                    <h1 className="text-xl">Astraea</h1>
                    <ul className="steps">
                        <li className="step step-primary">Draw Polygon</li>
                        <li className="step">Select Options</li>
                        <li className="step">Analyse Image</li>
                    </ul>
                    <div className="divider"></div>
                    {
                        step === 1 ? <DrawControl/> : 
                        step === 2 ? <ParameterSelection onAnalysisComplete={onAnalysisComplete} /> : 
                        <SearchOptions />
                    }
                </ul>
            </div>
        </div>
    );
}

export default SidebarAlt;