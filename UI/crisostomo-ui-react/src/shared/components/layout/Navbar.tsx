import React from "react";
import { API_URL } from "../../global/globalValues";

export const Navbar: React.FC = () => {
    return (
        <nav className="fixed top-0 left-0 w-full bg-black shadow-md z-50">
            <div className="flex items-center justify-between px-6 py-3">
            <div className="flex items-center cir">
                    <img 
                        src={API_URL+"/author/logo/100/100"} 
                        alt="logo" 
                        className="rounded-full bg-blend-luminosity h-12 w-12"
                    />
                  <span className="text-white font-bold ml-2 text-lg">Crisostomo</span>
                </div>
               

                {/* Links */}
                <div className="flex items-center gap-6 text-sm font-light text-white">
                    <a href="/dashboard" className="hover:text-gray-300">Dashboard</a>
                    <a href="/books" className="hover:text-gray-300">Books</a>
                    <a href="/authors" className="hover:text-gray-300">Authors</a>
                </div>
            </div>
        </nav>
    );
};
