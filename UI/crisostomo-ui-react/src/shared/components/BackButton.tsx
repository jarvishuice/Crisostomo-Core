import React from "react";
import { useNavigate } from "react-router-dom";
import type { BackButtonProps } from "../types/BackButtonProps";


const BackButton: React.FC<BackButtonProps> = ({ to }) => {
    const navigate = useNavigate();

    return (
        <button
            onClick={() => navigate(to)}
            className="flex items-center justify-center w-10 h-10 bg-white border border-gray-300 rounded-full hover:bg-gray-100 transition-colors"
            aria-label="Volver"
        >
            {/* Icono de flecha hacia atrás */}
            <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="w-6 h-6 text-black"
            >
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
        </button>
    );
};

export default BackButton;
